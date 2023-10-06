use arrow::temporal_conversions::{
    date32_to_datetime, timestamp_ms_to_datetime, timestamp_ns_to_datetime,
    timestamp_s_to_datetime, timestamp_us_to_datetime,
};
use datafusion::common::{Column, DataFusionError};
use datafusion::error::Result;
use datafusion::scalar::ScalarValue;
use datafusion_common::tree_node::{TreeNode, TreeNodeVisitor, VisitRecursion};
use datafusion_expr::expr::InList;
use datafusion_expr::{BinaryExpr, Expr, Operator};
use itertools::Itertools;

pub struct FilterPushdownVisitor<T: FilterPushdownConverter> {
    pub source: T,
    // LIFO stack for keeping the intermediate SQL expression results to be used in interpolation
    // of the parent nodes. After a successful visit, it should contain exactly one element, which
    // represents the complete SQL statement corresponding to the given expression.
    pub sql_exprs: Vec<String>,
}

impl<T: FilterPushdownConverter> FilterPushdownVisitor<T> {
    // Intended to be used in the node post-visit phase, ensuring that SQL representation of inner
    // nodes is on the stack.
    fn pop_sql_expr(&mut self) -> String {
        self.sql_exprs
            .pop()
            .expect("No SQL expression in the stack")
    }
}

pub struct PostgresFilterPushdown {}

impl FilterPushdownConverter for PostgresFilterPushdown {}

pub trait FilterPushdownConverter {
    fn col_to_sql(&self, col: &Column) -> String {
        quote_identifier_double_quotes(&col.name)
    }

    fn scalar_value_to_sql(&self, value: &ScalarValue) -> Option<String> {
        match value {
            ScalarValue::Utf8(Some(val)) | ScalarValue::LargeUtf8(Some(val)) => {
                Some(format!("'{}'", val.replace('\'', "''")))
            }
            ScalarValue::Date32(Some(days)) => {
                let date = date32_to_datetime(*days)?.date();
                Some(format!("'{date}'"))
            }
            ScalarValue::Date64(Some(t_ms))
            | ScalarValue::TimestampMillisecond(Some(t_ms), None) => {
                let timestamp = timestamp_ms_to_datetime(*t_ms)?;
                Some(format!("'{timestamp}'"))
            }
            ScalarValue::TimestampSecond(Some(t_s), None) => {
                let timestamp = timestamp_s_to_datetime(*t_s)?;
                Some(format!("'{timestamp}'"))
            }
            ScalarValue::TimestampMicrosecond(Some(t_us), None) => {
                let timestamp = timestamp_us_to_datetime(*t_us)?;
                Some(format!("'{timestamp}'"))
            }
            ScalarValue::TimestampNanosecond(Some(t_ns), None) => {
                let timestamp = timestamp_ns_to_datetime(*t_ns)?;
                Some(format!("'{timestamp}'"))
            }
            ScalarValue::TimestampSecond(_, Some(_))
            | ScalarValue::TimestampMillisecond(_, Some(_))
            | ScalarValue::TimestampMicrosecond(_, Some(_))
            | ScalarValue::TimestampNanosecond(_, Some(_)) => None,
            _ => Some(format!("{value}")),
        }
    }

    fn op_to_sql(&self, op: &Operator) -> Option<String> {
        Some(op.to_string())
    }
}

impl<T: FilterPushdownConverter> TreeNodeVisitor for FilterPushdownVisitor<T> {
    type N = Expr;

    fn pre_visit(&mut self, expr: &Expr) -> Result<VisitRecursion> {
        match expr {
            Expr::Column(_)
            | Expr::Literal(_)
            | Expr::Not(_)
            | Expr::Negative(_)
            | Expr::IsNull(_)
            | Expr::IsNotNull(_)
            | Expr::IsTrue(_)
            | Expr::IsFalse(_)
            | Expr::IsNotTrue(_)
            | Expr::IsNotFalse(_)
            | Expr::InList { .. } => {}
            Expr::BinaryExpr(BinaryExpr { op, .. }) => {
                // Check if operator pushdown supported; left and right expressions will be checked
                // through further recursion.
                if self.source.op_to_sql(op).is_none() {
                    return Err(DataFusionError::Execution(format!(
                        "Operator {op} not shippable",
                    )));
                }
            }
            _ => {
                // Expression is not supported, no need to visit any remaining child or parent nodes
                return Err(DataFusionError::Execution(format!(
                    "Expression {expr:?} not shippable",
                )));
            }
        };
        Ok(VisitRecursion::Continue)
    }

    fn post_visit(&mut self, expr: &Expr) -> Result<VisitRecursion> {
        match expr {
            // Column and Literal are the only two leaf nodes atm - they don't depend on any SQL
            // expression being on the stack.
            Expr::Column(col) => self.sql_exprs.push(self.source.col_to_sql(col)),
            Expr::Literal(val) => {
                let sql_val = self.source.scalar_value_to_sql(val).ok_or_else(|| {
                    DataFusionError::Execution(format!("ScalarValue {val:?} not shippable",))
                })?;
                self.sql_exprs.push(sql_val)
            }
            Expr::BinaryExpr(be @ BinaryExpr { .. }) => {
                // The visitor has been through left and right sides in that order, so the topmost
                // item on the SQL expression stack is the right expression
                let mut right_sql = self.pop_sql_expr();
                let mut left_sql = self.pop_sql_expr();

                // Similar as in Display impl for BinaryExpr: since the Expr has an implicit operator
                // precedence we need to convert it to an explicit one using extra parenthesis if the
                // left/right expression is also a BinaryExpr of lower operator precedence.
                if let Expr::BinaryExpr(right_be @ BinaryExpr { .. }) = &*be.right {
                    let p = right_be.op.precedence();
                    if p == 0 || p < be.op.precedence() {
                        right_sql = format!("({right_sql})")
                    }
                }
                if let Expr::BinaryExpr(left_be @ BinaryExpr { .. }) = &*be.left {
                    let p = left_be.op.precedence();
                    if p == 0 || p < be.op.precedence() {
                        left_sql = format!("({left_sql})")
                    }
                }

                let op_sql = self.source.op_to_sql(&be.op).ok_or_else(|| {
                    DataFusionError::Execution(format!(
                        "Couldn't convert operator {:?} to a compatible one for the remote system",
                        be.op,
                    ))
                })?;

                self.sql_exprs
                    .push(format!("{left_sql} {op_sql} {right_sql}"))
            }
            Expr::Not(_) => {
                let inner_sql = self.pop_sql_expr();
                self.sql_exprs.push(format!("NOT {inner_sql}"));
            }
            Expr::Negative(_) => {
                let inner_sql = self.pop_sql_expr();
                self.sql_exprs.push(format!("(- {inner_sql})"));
            }
            Expr::IsNull(_) => {
                let inner_sql = self.pop_sql_expr();
                self.sql_exprs.push(format!("{inner_sql} IS NULL"));
            }
            Expr::IsNotNull(_) => {
                let inner_sql = self.pop_sql_expr();
                self.sql_exprs.push(format!("{inner_sql} IS NOT NULL"));
            }
            Expr::IsTrue(_) => {
                let inner_sql = self.pop_sql_expr();
                self.sql_exprs.push(format!("{inner_sql} IS TRUE"));
            }
            Expr::IsFalse(_) => {
                let inner_sql = self.pop_sql_expr();
                self.sql_exprs.push(format!("{inner_sql} IS FALSE"));
            }
            Expr::IsNotTrue(_) => {
                let inner_sql = self.pop_sql_expr();
                self.sql_exprs.push(format!("{inner_sql} IS NOT TRUE"));
            }
            Expr::IsNotFalse(_) => {
                let inner_sql = self.pop_sql_expr();
                self.sql_exprs.push(format!("{inner_sql} IS NOT FALSE"));
            }
            Expr::InList(InList { list, negated, .. }) => {
                // The N elements of the list are on the top of the stack, we need to pop them first
                let index = self.sql_exprs.len() - list.len();
                let list_sql = self.sql_exprs.split_off(index).iter().join(", ");
                // Now consume the expression
                let expr_sql = self.pop_sql_expr();
                if *negated {
                    self.sql_exprs
                        .push(format!("{expr_sql} NOT IN ({list_sql})"));
                } else {
                    self.sql_exprs.push(format!("{expr_sql} IN ({list_sql})"));
                }
            }
            _ => {}
        };
        Ok(VisitRecursion::Continue)
    }
}

pub fn quote_identifier_double_quotes(name: &str) -> String {
    format!("\"{}\"", name.replace('\"', "\"\""))
}

// Walk the filter expression AST for a particular remote source type and see if the expression is
// ship-able, at the same time converting elements (e.g. operators) to the native representation if
// needed.
pub fn filter_expr_to_sql<T: FilterPushdownConverter>(filter: &Expr, source: T) -> Result<String> {
    // Construct the initial visitor state
    let mut visitor = FilterPushdownVisitor {
        source,
        sql_exprs: vec![],
    };

    // Perform the walk through the expr AST trying to construct the equivalent SQL for the
    // particular source type at hand.
    filter.visit(&mut visitor)?;
    let sql_exprs = visitor.sql_exprs;

    if sql_exprs.len() != 1 {
        return Err(DataFusionError::Execution(format!(
            "Expected exactly one SQL expression for filter {filter}, found: {sql_exprs:?}",
        )));
    }

    Ok(sql_exprs
        .first()
        .expect("Exactly 1 SQL expression expected")
        .clone())
}
