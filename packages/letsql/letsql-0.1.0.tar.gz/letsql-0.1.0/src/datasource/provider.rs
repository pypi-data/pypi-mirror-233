use std::any::Any;
use std::ops::Deref;
use std::sync::Arc;

use super::filter_pushdown::{
    filter_expr_to_sql, quote_identifier_double_quotes, PostgresFilterPushdown,
};
use arrow_schema::SchemaRef;
use async_trait::async_trait;
use connectorx::destinations::arrow::ArrowDestination;
use connectorx::prelude::{get_arrow, CXQuery, SourceConn, SourceType};
use datafusion::common::DataFusionError;
use datafusion::datasource::TableProvider;
use datafusion::error::Result;
use datafusion::execution::context::SessionState;
use datafusion::physical_plan::memory::MemoryExec;
use datafusion::physical_plan::ExecutionPlan;
use datafusion_expr::{Expr, TableType};
use datafusion_optimizer::utils::conjunction;
use tokio::task;

pub struct RemoteTable {
    name: Arc<str>,
    schema: SchemaRef,
    source_conn: SourceConn,
}

impl RemoteTable {
    pub async fn new(name: String, conn: String, schema: SchemaRef) -> Result<Self> {
        let source_conn = SourceConn::try_from(conn.as_str()).map_err(|e| {
            DataFusionError::Execution(format!(
                "Failed initialising the remote table connection {e:?}"
            ))
        })?;

        let mut remote_table = Self {
            name: Arc::from(name.clone()),
            schema: schema.clone(),
            source_conn,
        };

        if schema.fields().is_empty() {
            let one_row = vec![CXQuery::from(
                format!("SELECT * FROM {name} LIMIT 1").as_str(),
            )];

            // Introspect the schema
            let one_row_schema = remote_table
                .run_queries(one_row)
                .await?
                .arrow_schema()
                .deref()
                .clone();
            remote_table.schema = Arc::new(one_row_schema);
        }

        Ok(remote_table)
    }

    async fn run_queries(&self, queries: Vec<CXQuery<String>>) -> Result<ArrowDestination> {
        let source_conn = self.source_conn.clone();

        task::spawn_blocking(move || {
            get_arrow(&source_conn, None, queries.as_slice()).map_err(|e| {
                DataFusionError::Execution(format!("Failed running the remote query {e:?}"))
            })
        })
        .await
        .map_err(|e| {
            DataFusionError::Execution(format!("Failed executing the remote query {e:?}"))
        })?
    }

    // Convert the DataFusion expression representing a filter to an equivalent SQL string for the
    // remote data source if the entire filter can be pushed down.
    fn filter_expr_to_sql(&self, filter: &Expr) -> Option<String> {
        let result = match self.source_conn.ty {
            SourceType::Postgres => filter_expr_to_sql(filter, PostgresFilterPushdown {}),
            _ => {
                return None;
            }
        };

        result
            .map_err(|err| print!("Failed constructing SQL for filter {filter}: {err}"))
            .ok()
    }
}

#[async_trait]
impl TableProvider for RemoteTable {
    fn as_any(&self) -> &dyn Any {
        self
    }

    fn schema(&self) -> SchemaRef {
        self.schema.clone()
    }

    fn table_type(&self) -> TableType {
        TableType::View
    }

    async fn scan(
        &self,
        _state: &SessionState,
        projection: Option<&Vec<usize>>,
        filters: &[Expr],
        limit: Option<usize>,
    ) -> Result<Arc<dyn ExecutionPlan>> {
        let schema = self.schema.deref().clone();
        let mut columns = "*".to_string();

        if let Some(indices) = projection {
            let schema = schema.project(indices).unwrap();
            columns = schema
                .fields()
                .iter()
                .map(|f| quote_identifier_double_quotes(f.name()))
                .collect::<Vec<String>>()
                .join(", ")
        }

        // Apply LIMIT if any
        let limit_clause = limit.map_or("".to_string(), |size| format!(" LIMIT {size}"));

        // Try to construct the WHERE clause: all passed filters should be eligible for pushdown as
        // they've past the checks in `supports_filter_pushdown`
        let where_clause = if filters.is_empty() {
            "".to_string()
        } else {
            // NB: Given that all supplied filters have passed the shipabilty check individually,
            // there should be no harm in merging them together and converting that to equivalent SQL
            let merged_filter = conjunction(filters.to_vec()).ok_or_else(|| {
                DataFusionError::Execution(format!(
                    "Failed merging received filters into one {filters:?}"
                ))
            })?;
            let filters_sql = self.filter_expr_to_sql(&merged_filter).ok_or_else(|| {
                DataFusionError::Execution(format!(
                    "Failed converting filter to SQL {merged_filter}"
                ))
            })?;
            format!(" WHERE {filters_sql}")
        };

        // Construct and run the remote query
        let queries = vec![CXQuery::from(
            format!(
                "SELECT {} FROM {}{}{}",
                columns, self.name, where_clause, limit_clause
            )
            .as_str(),
        )];

        let arrow_data = self.run_queries(queries).await?;
        let src_schema = arrow_data.arrow_schema().deref().clone();
        let data = arrow_data.arrow().map_err(|e| {
            DataFusionError::Execution(format!("Failed extracting the fetched data {e:?}"))
        })?;

        let wrap_data = data.into_iter().map(|rb| vec![rb]).collect::<Vec<_>>();

        let plan: Arc<dyn ExecutionPlan> = Arc::new(MemoryExec::try_new(
            wrap_data.as_slice(),
            Arc::new(src_schema),
            None,
        )?);

        Ok(plan)
    }
}
