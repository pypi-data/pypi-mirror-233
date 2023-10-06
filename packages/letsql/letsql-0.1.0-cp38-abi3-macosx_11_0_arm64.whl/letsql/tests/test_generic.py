from __future__ import annotations

import contextlib
import datetime
import decimal
from operator import invert, methodcaller, neg

import numpy as np
import pandas as pd
import pandas.testing as tm
import pytest
import toolz
from pytest import param

import letsql._vendor.ibis as ibis
import letsql._vendor.ibis.common.exceptions as com
import letsql._vendor.ibis.expr.datatypes as dt
import letsql._vendor.ibis.selectors as s
from letsql._vendor.ibis import _
from letsql._vendor.ibis.common.annotations import ValidationError
from letsql.tests.base import (
    assert_frame_equal,
    assert_series_equal,
    default_series_rename,
)

NULL_BACKEND_TYPES = "NULL"


def test_null_literal(con):
    expr = ibis.null()
    result = con.execute(expr)
    assert result is None

    with contextlib.suppress(com.OperationNotDefinedError):
        assert con.execute(expr.typeof()) == "NULL"


def test_boolean_literal(con):
    expr = ibis.literal(False, type=dt.boolean)
    result = con.execute(expr)
    assert not result
    assert type(result) in (np.bool_, bool)


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        param(
            ibis.NA.fillna(5),
            5,
            id="na_fillna",
        ),
        param(
            ibis.literal(5).fillna(10),
            5,
            id="non_na_fillna",
        ),
        param(ibis.literal(5).nullif(5), None, id="nullif_null"),
        param(ibis.literal(10).nullif(5), 10, id="nullif_not_null"),
    ],
)
def test_scalar_fillna_nullif(con, expr, expected):
    if expected is None:
        assert pd.isna(con.execute(expr))
    else:
        assert con.execute(expr) == expected


@pytest.mark.parametrize(
    ("col", "filt"),
    [
        param(
            "nan_col",
            _.nan_col.isnan(),
            marks=pytest.mark.notimpl(raises=com.OperationNotDefinedError),
            id="nan_col",
        ),
        param(
            "none_col",
            _.none_col.isnull(),
            marks=[pytest.mark.notimpl(raises=com.OperationNotDefinedError)],
            id="none_col",
        ),
    ],
)
def test_isna(alltypes, col, filt):
    table = alltypes.select(
        nan_col=ibis.literal(np.nan), none_col=ibis.NA.cast("float64")
    )
    df = table.execute()

    result = table[filt].execute().reset_index(drop=True)
    expected = df[df[col].isna()].reset_index(drop=True)

    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "value",
    [
        None,
        param(
            np.nan,
            marks=pytest.mark.notimpl(
                raises=AssertionError,
                reason="NaN != NULL",
            ),
            id="nan_col",
        ),
    ],
)
def test_column_fillna(alltypes, value):
    table = alltypes.mutate(missing=ibis.literal(value).cast("float64"))
    pd_table = table.execute()

    res = table.mutate(missing=table.missing.fillna(0.0)).execute()
    sol = pd_table.assign(missing=pd_table.missing.fillna(0.0))
    assert_frame_equal(res.reset_index(drop=True), sol.reset_index(drop=True))


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        param(ibis.coalesce(5, None, 4), 5, id="generic"),
        param(ibis.coalesce(ibis.NA, 4, ibis.NA), 4, id="null_start_end"),
        param(ibis.coalesce(ibis.NA, ibis.NA, 3.14), 3.14, id="non_null_last"),
    ],
)
def test_coalesce(con, expr, expected):
    result = con.execute(expr.name("tmp"))

    if isinstance(result, decimal.Decimal):
        # in case of Impala the result is decimal
        # >>> decimal.Decimal('5.56') == 5.56
        # False
        assert result == decimal.Decimal(str(expected))
    else:
        assert result == pytest.approx(expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_identical_to(alltypes, sorted_df):
    sorted_alltypes = alltypes.order_by("id")
    df = sorted_df
    dt = df[["tinyint_col", "double_col"]]

    ident = sorted_alltypes.tinyint_col.identical_to(sorted_alltypes.double_col)
    expr = sorted_alltypes["id", ident.name("tmp")].order_by("id")
    result = expr.execute().tmp

    expected = (dt.tinyint_col.isnull() & dt.double_col.isnull()) | (
        dt.tinyint_col == dt.double_col
    )

    expected = default_series_rename(expected)
    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    ("column", "elements"),
    [
        ("int_col", [1, 2, 3]),
        ("int_col", (1, 2, 3)),
        ("string_col", ["1", "2", "3"]),
        ("string_col", ("1", "2", "3")),
        ("int_col", {1}),
        ("int_col", frozenset({1})),
    ],
)
def test_isin(alltypes, sorted_df, column, elements):
    sorted_alltypes = alltypes.order_by("id")
    expr = sorted_alltypes[
        "id", sorted_alltypes[column].isin(elements).name("tmp")
    ].order_by("id")
    result = expr.execute().tmp

    expected = sorted_df[column].isin(elements)
    expected = default_series_rename(expected)
    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    ("column", "elements"),
    [
        ("int_col", [1, 2, 3]),
        ("int_col", (1, 2, 3)),
        ("string_col", ["1", "2", "3"]),
        ("string_col", ("1", "2", "3")),
        ("int_col", {1}),
        ("int_col", frozenset({1})),
    ],
)
def test_notin(alltypes, sorted_df, column, elements):
    sorted_alltypes = alltypes.order_by("id")
    expr = sorted_alltypes[
        "id", sorted_alltypes[column].notin(elements).name("tmp")
    ].order_by("id")
    result = expr.execute().tmp

    expected = ~sorted_df[column].isin(elements)
    expected = default_series_rename(expected)
    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    ("predicate_fn", "expected_fn"),
    [
        param(lambda t: t["bool_col"], lambda df: df["bool_col"], id="no_op"),
        param(lambda t: ~t["bool_col"], lambda df: ~df["bool_col"], id="negate"),
        param(
            lambda t: t.bool_col & t.bool_col,
            lambda df: df.bool_col & df.bool_col,
            id="and",
        ),
        param(
            lambda t: t.bool_col | t.bool_col,
            lambda df: df.bool_col | df.bool_col,
            id="or",
        ),
        param(
            lambda t: t.bool_col ^ t.bool_col,
            lambda df: df.bool_col ^ df.bool_col,
            id="xor",
            marks=pytest.mark.notimpl(raises=com.OperationNotDefinedError),
        ),
    ],
)
def test_filter(alltypes, sorted_df, predicate_fn, expected_fn):
    sorted_alltypes = alltypes.order_by("id")
    table = sorted_alltypes[predicate_fn(sorted_alltypes)].order_by("id")
    result = table.execute()
    expected = sorted_df[expected_fn(sorted_df)]

    assert_frame_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_filter_with_window_op(alltypes, sorted_df):
    sorted_alltypes = alltypes.order_by("id")
    table = sorted_alltypes
    window = ibis.window(group_by=table.id)
    table = table.filter(lambda t: t["id"].mean().over(window) > 3).order_by("id")
    result = table.execute()
    expected = (
        sorted_df.groupby(["id"])
        .filter(lambda t: t["id"].mean() > 3)
        .reset_index(drop=True)
    )
    assert_frame_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_case_where(alltypes, df):
    table = alltypes
    table = table.mutate(
        new_col=(
            ibis.case()
            .when(table["int_col"] == 1, 20)
            .when(table["int_col"] == 0, 10)
            .else_(0)
            .end()
            .cast("int64")
        )
    )

    result = table.execute()

    expected = df.copy()
    mask_0 = expected["int_col"] == 1
    mask_1 = expected["int_col"] == 0

    expected["new_col"] = 0
    expected.loc[mask_0, "new_col"] = 20
    expected.loc[mask_1, "new_col"] = 10

    assert_frame_equal(result, expected)


# TODO: some of these are notimpl (datafusion) others are probably never
@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_select_filter_mutate(alltypes, df):
    """Test that select, filter and mutate are executed in right order.

    Before PR #2635, try_fusion in analysis.py would fuse these
    operations together in a way that the order of the operations were
    wrong. (mutate was executed before filter).
    """
    t = alltypes

    # Prepare the float_col so that filter must execute
    # before the cast to get the correct result.
    t = t.mutate(
        float_col=ibis.case().when(t["bool_col"], t["float_col"]).else_(np.nan).end()
    )

    # Actual test
    t = t[t.columns]
    t = t[~t["float_col"].isnan()]
    t = t.mutate(float_col=t["float_col"].cast("float64"))
    result = t.execute()

    expected = df.copy()
    expected.loc[~df["bool_col"], "float_col"] = None
    expected = expected[~expected["float_col"].isna()].reset_index(drop=True)
    expected = expected.assign(float_col=expected["float_col"].astype("float64"))

    assert_series_equal(result.float_col, expected.float_col)


def test_table_fillna_invalid(alltypes):
    with pytest.raises(
        com.IbisTypeError, match=r"Column 'invalid_col' is not found in table"
    ):
        alltypes.fillna({"invalid_col": 0.0})

    with pytest.raises(
        com.IbisTypeError, match="Cannot fillna on column 'string_col' of type.*"
    ):
        alltypes[["int_col", "string_col"]].fillna(0)

    with pytest.raises(
        com.IbisTypeError, match="Cannot fillna on column 'int_col' of type.*"
    ):
        alltypes.fillna({"int_col": "oops"})


@pytest.mark.parametrize(
    "replacements",
    [
        {"int_col": 20},
        {"double_col": -1, "string_col": "missing"},
        {"double_col": -1.5, "string_col": "missing"},
    ],
)
@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_table_fillna_mapping(alltypes, replacements):
    table = alltypes.mutate(
        int_col=alltypes.int_col.nullif(1),
        double_col=alltypes.double_col.nullif(3.0),
        string_col=alltypes.string_col.nullif("2"),
    ).select("id", "int_col", "double_col", "string_col")
    pd_table = table.execute()

    result = table.fillna(replacements).execute().reset_index(drop=True)
    expected = pd_table.fillna(replacements).reset_index(drop=True)

    assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_table_fillna_scalar(alltypes):
    table = alltypes.mutate(
        int_col=alltypes.int_col.nullif(1),
        double_col=alltypes.double_col.nullif(3.0),
        string_col=alltypes.string_col.nullif("2"),
    ).select("id", "int_col", "double_col", "string_col")
    pd_table = table.execute()

    res = table[["int_col", "double_col"]].fillna(0).execute().reset_index(drop=True)
    sol = pd_table[["int_col", "double_col"]].fillna(0).reset_index(drop=True)
    assert_frame_equal(res, sol, check_dtype=False)

    res = table[["string_col"]].fillna("missing").execute().reset_index(drop=True)
    sol = pd_table[["string_col"]].fillna("missing").reset_index(drop=True)
    assert_frame_equal(res, sol, check_dtype=False)


def test_mutate_rename(alltypes):
    table = alltypes.select(["bool_col", "string_col"])
    table = table.mutate(dupe_col=table["bool_col"])
    result = table.execute()
    # check_dtype is False here because there are dtype diffs between
    # Pyspark and Pandas on Java 8 - filling the 'none_col' with an int
    # results in float in Pyspark, and int in Pandas. This diff does
    # not exist in Java 11.
    assert list(result.columns) == ["bool_col", "string_col", "dupe_col"]


def test_dropna_invalid(alltypes):
    with pytest.raises(
        com.IbisTypeError, match=r"Column 'invalid_col' is not found in table"
    ):
        alltypes.dropna(subset=["invalid_col"])

    with pytest.raises(ValidationError):
        alltypes.dropna(how="invalid")


@pytest.mark.parametrize("how", ["any", "all"])
@pytest.mark.parametrize(
    "subset", [None, [], "col_1", ["col_1", "col_2"], ["col_1", "col_3"]]
)
@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_dropna_table(alltypes, how, subset):
    is_two = alltypes.int_col == 2
    is_four = alltypes.int_col == 4

    table = alltypes.mutate(
        col_1=is_two.ifelse(ibis.NA, alltypes.float_col),
        col_2=is_four.ifelse(ibis.NA, alltypes.float_col),
        col_3=(is_two | is_four).ifelse(ibis.NA, alltypes.float_col),
    ).select("col_1", "col_2", "col_3")

    table_pandas = table.execute()
    result = table.dropna(subset, how).execute().reset_index(drop=True)
    expected = table_pandas.dropna(how=how, subset=subset).reset_index(drop=True)

    assert_frame_equal(result, expected)


def test_select_sort_sort(alltypes):
    query = alltypes[alltypes.year, alltypes.bool_col]
    query = query.order_by(query.year).order_by(query.bool_col)


@pytest.mark.parametrize(
    "key, df_kwargs",
    [
        param("id", {"by": "id"}),
        param(_.id, {"by": "id"}),
        param(lambda _: _.id, {"by": "id"}),
        param(
            ibis.desc("id"),
            {"by": "id", "ascending": False},
        ),
        param(
            ["id", "int_col"],
            {"by": ["id", "int_col"]},
        ),
        param(
            ["id", ibis.desc("int_col")],
            {"by": ["id", "int_col"], "ascending": [True, False]},
        ),
    ],
)
def test_order_by(alltypes, df, key, df_kwargs):
    result = alltypes.filter(_.id < 100).order_by(key).execute()
    expected = df.loc[df.id < 100].sort_values(**df_kwargs)
    assert_frame_equal(result, expected)


def test_order_by_random(alltypes):
    expr = alltypes.filter(_.id < 100).order_by(ibis.random()).limit(5)
    r1 = expr.execute()
    r2 = expr.execute()
    assert len(r1) == 5
    assert len(r2) == 5
    # Ensure that multiple executions returns different results
    assert not r1.equals(r2)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_table_info(alltypes):
    expr = alltypes.info()
    df = expr.execute()
    assert alltypes.columns == list(df.name)
    assert expr.columns == [
        "name",
        "type",
        "nullable",
        "nulls",
        "non_nulls",
        "null_frac",
        "pos",
    ]
    assert expr.columns == list(df.columns)


@pytest.mark.parametrize(
    ("ibis_op", "pandas_op"),
    [
        param(
            _.string_col.isin([]),
            lambda df: df.string_col.isin([]),
            id="isin",
        ),
        param(
            _.string_col.notin([]),
            lambda df: ~df.string_col.isin([]),
            id="notin",
        ),
        param(
            (_.string_col.length() * 1).isin([1]),
            lambda df: (df.string_col.str.len() * 1).isin([1]),
            id="isin_non_empty",
        ),
        param(
            (_.string_col.length() * 1).notin([1]),
            lambda df: ~(df.string_col.str.len() * 1).isin([1]),
            id="notin_non_empty",
        ),
    ],
)
def test_isin_notin(alltypes, df, ibis_op, pandas_op):
    expr = alltypes[ibis_op]
    expected = df.loc[pandas_op(df)].sort_values(["id"]).reset_index(drop=True)
    result = expr.execute().sort_values(["id"]).reset_index(drop=True)
    assert_frame_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
@pytest.mark.parametrize(
    ("ibis_op", "pandas_op"),
    [
        param(
            _.string_col.isin(_.string_col),
            lambda df: df.string_col.isin(df.string_col),
            id="isin_col",
        ),
        param(
            (_.bigint_col + 1).isin(_.string_col.length() + 1),
            lambda df: df.bigint_col.add(1).isin(df.string_col.str.len().add(1)),
            id="isin_expr",
        ),
        param(
            _.string_col.notin(_.string_col),
            lambda df: ~df.string_col.isin(df.string_col),
            id="notin_col",
        ),
        param(
            (_.bigint_col + 1).notin(_.string_col.length() + 1),
            lambda df: ~(df.bigint_col.add(1)).isin(df.string_col.str.len().add(1)),
            id="notin_expr",
        ),
    ],
)
def test_isin_notin_column_expr(alltypes, df, ibis_op, pandas_op):
    expr = alltypes[ibis_op].order_by("id")
    expected = df[pandas_op(df)].sort_values(["id"]).reset_index(drop=True)
    result = expr.execute()
    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    ("expr", "expected", "op"),
    [
        param(True, True, toolz.identity, id="true_noop"),
        param(False, False, toolz.identity, id="false_noop"),
        param(
            True,
            False,
            invert,
            id="true_invert",
        ),
        param(
            False,
            True,
            invert,
            id="false_invert",
        ),
        param(True, False, neg, id="true_negate"),
        param(
            False,
            True,
            neg,
            id="false_negate",
        ),
    ],
)
def test_logical_negation_literal(con, expr, expected, op):
    assert con.execute(op(ibis.literal(expr)).name("tmp")) == expected


@pytest.mark.parametrize(
    "op",
    [
        toolz.identity,
        invert,
        neg,
    ],
)
def test_logical_negation_column(alltypes, df, op):
    result = op(alltypes["bool_col"]).name("tmp").execute()
    expected = op(df["bool_col"])
    assert_series_equal(result, expected, check_names=False)


@pytest.mark.parametrize(
    ("dtype", "zero", "expected"),
    [("int64", 0, 1), ("float64", 0.0, 1.0)],
)
def test_zeroifnull_literals(con, dtype, zero, expected):
    assert con.execute(ibis.NA.cast(dtype).zeroifnull()) == zero
    assert con.execute(ibis.literal(expected, type=dtype).zeroifnull()) == expected


def test_zeroifnull_column(alltypes, df):
    expr = alltypes.int_col.nullif(1).zeroifnull().name("tmp")
    result = expr.execute().astype("int32")
    expected = df.int_col.replace(1, 0).rename("tmp").astype("int32")
    assert_series_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_ifelse_select(alltypes, df):
    table = alltypes
    table = table.select(
        [
            "int_col",
            (
                ibis.ifelse(table["int_col"] == 0, 42, -1)
                .cast("int64")
                .name("where_col")
            ),
        ]
    )

    result = table.execute()

    expected = df.loc[:, ["int_col"]].copy()

    expected["where_col"] = -1
    expected.loc[expected["int_col"] == 0, "where_col"] = 42

    assert_frame_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_ifelse_column(alltypes, df):
    expr = ibis.ifelse(alltypes["int_col"] == 0, 42, -1).cast("int64").name("where_col")
    result = expr.execute()

    expected = pd.Series(
        np.where(df.int_col == 0, 42, -1),
        name="where_col",
        dtype="int64",
    )

    assert_series_equal(result, expected)


def test_select_filter(alltypes, df):
    t = alltypes

    expr = t.select("int_col").filter(t.string_col == "4")
    result = expr.execute()

    expected = df.loc[df.string_col == "4", ["int_col"]].reset_index(drop=True)
    assert_frame_equal(result, expected)


def test_select_filter_select(alltypes, df):
    t = alltypes
    expr = t.select("int_col").filter(t.string_col == "4").int_col
    result = expr.execute().rename("int_col")

    expected = df.loc[df.string_col == "4", "int_col"].reset_index(drop=True)
    assert_series_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_between(alltypes, df):
    expr = alltypes.double_col.between(5, 10)
    result = expr.execute().rename("double_col")

    expected = df.double_col.between(5, 10)
    assert_series_equal(result, expected)


def test_interactive(alltypes, monkeypatch):
    monkeypatch.setattr(ibis.options, "interactive", True)

    expr = alltypes.mutate(
        str_col=_.string_col.replace("1", "").nullif("2"),
        date_col=_.timestamp_col.date(),
        delta_col=lambda t: ibis.now() - t.timestamp_col,
    )

    repr(expr)


def test_correlated_subquery(alltypes):
    expr = alltypes[_.double_col > _.view().double_col]
    assert expr.compile() is not None


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_uncorrelated_subquery(batting, batting_df):
    subset_batting = batting[batting.yearID <= 2000]
    expr = batting[_.yearID == subset_batting.yearID.max()]["playerID", "yearID"]
    result = expr.execute()

    expected = batting_df[batting_df.yearID == 2000][["playerID", "yearID"]]
    assert_frame_equal(result, expected)


def test_int_column(alltypes):
    expr = alltypes.mutate(x=1).x
    result = expr.execute()
    assert expr.type() == dt.int8
    assert result.dtype == np.int8


def test_int_scalar(alltypes):
    expr = alltypes.smallint_col.min()
    result = expr.execute()
    assert expr.type() == dt.int16
    assert result.dtype == np.int16


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
@pytest.mark.parametrize("method_name", ["any", "notany"])
def test_exists(batting, awards_players, method_name):
    years = [1980, 1981]
    batting_years = [1871, *years]
    batting = batting[batting.yearID.isin(batting_years)]
    awards_players = awards_players[awards_players.yearID.isin(years)]
    method = methodcaller(method_name)
    expr = batting[method(batting.yearID == awards_players.yearID)]
    result = expr.execute()
    assert not result.empty


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_typeof(con):
    # Other tests also use the typeof operation, but only this test has this operation required.
    expr = ibis.literal(1).typeof()
    result = con.execute(expr)

    assert result is not None


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_isin_uncorrelated(batting, awards_players, batting_df, awards_players_df):
    expr = batting.select(
        "playerID",
        "yearID",
        has_year_id=batting.yearID.isin(awards_players.yearID),
    ).order_by(["playerID", "yearID"])
    result = expr.execute().has_year_id
    expected = (
        batting_df.sort_values(["playerID", "yearID"])
        .reset_index(drop=True)
        .yearID.isin(awards_players_df.yearID)
        .rename("has_year_id")
    )
    assert_series_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_isin_uncorrelated_filter(
    batting, awards_players, batting_df, awards_players_df
):
    expr = (
        batting.select("playerID", "yearID")
        .filter(batting.yearID.isin(awards_players.yearID))
        .order_by(["playerID", "yearID"])
    )
    result = expr.execute()
    expected = (
        batting_df.loc[
            batting_df.yearID.isin(awards_players_df.yearID), ["playerID", "yearID"]
        ]
        .sort_values(["playerID", "yearID"])
        .reset_index(drop=True)
    )
    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "dtype",
    [
        "bool",
        "bytes",
        "str",
        "int",
        "float",
        "int8",
        "int16",
        "int32",
        "int64",
        "float32",
        "float64",
        "timestamp",
        "date",
        "time",
    ],
)
def test_literal_na(con, dtype):
    expr = ibis.literal(None, type=dtype)
    result = con.execute(expr)
    assert pd.isna(result)


def test_memtable_bool_column(con):
    t = ibis.memtable({"a": [True, False, True]})
    assert_series_equal(con.execute(t.a), pd.Series([True, False, True], name="a"))


def test_memtable_construct(con, monkeypatch):
    pa = pytest.importorskip("pyarrow")
    monkeypatch.setattr(ibis.options, "default_backend", con)

    pa_t = pa.Table.from_pydict(
        {
            "a": list("abc"),
            "b": [1, 2, 3],
            "c": [1.0, 2.0, 3.0],
            "d": [None, "b", None],
        }
    )
    t = ibis.memtable(pa_t)
    assert_frame_equal(t.execute().fillna(pd.NA), pa_t.to_pandas().fillna(pd.NA))


@pytest.mark.notimpl(
    reason="backend doesn't support arrays and we don't implement pivot_longer with unions yet",
    raises=com.OperationNotDefinedError,
)
def test_pivot_longer(diamonds):
    df = diamonds.execute()
    res = diamonds.pivot_longer(s.c("x", "y", "z"), names_to="pos", values_to="xyz")
    assert res.schema().names == (
        "carat",
        "cut",
        "color",
        "clarity",
        "depth",
        "table",
        "price",
        "pos",
        "xyz",
    )
    expected = pd.melt(
        df,
        id_vars=[
            "carat",
            "cut",
            "color",
            "clarity",
            "depth",
            "table",
            "price",
        ],
        value_vars=list("xyz"),
        var_name="pos",
        value_name="xyz",
    )
    assert len(res.execute()) == len(expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_pivot_wider(diamonds):
    expr = (
        diamonds.group_by(["cut", "color"])
        .agg(carat=_.carat.mean())
        .pivot_wider(
            names_from="cut", values_from="carat", names_sort=True, values_agg="mean"
        )
    )
    df = expr.execute()
    assert set(df.columns) == {"color"} | set(
        diamonds[["cut"]].distinct().cut.execute()
    )
    assert len(df) == diamonds.color.nunique().execute()


@pytest.mark.parametrize(
    "on",
    [
        param(
            ["cut"],
            id="one",
        ),
        param(
            ["clarity", "cut"],
            id="many",
        ),
    ],
)
@pytest.mark.parametrize(
    "keep",
    ["first", "last"],
)
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
    reason="backend doesn't implement window functions",
)
def test_distinct_on_keep(on, keep, diamonds):
    from letsql._vendor.ibis import _

    t = diamonds.mutate(one=ibis.literal(1)).mutate(
        idx=ibis.row_number().over(order_by=_.one, rows=(None, 0))
    )

    expr = t.distinct(on=on, keep=keep).order_by(ibis.asc("idx"))
    result = expr.execute()
    df = t.execute()
    expected = (
        df.drop_duplicates(subset=on, keep=keep or False)
        .sort_values(by=["idx"])
        .reset_index(drop=True)
    )
    assert len(result) == len(expected)


@pytest.mark.parametrize(
    "on",
    [
        param(
            ["cut"],
            id="one",
        ),
        param(
            ["clarity", "cut"],
            id="many",
        ),
    ],
)
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
    reason="backend doesn't implement window functions",
)
def test_distinct_on_keep_is_none(on, diamonds):
    from letsql._vendor.ibis import _

    t = diamonds.mutate(one=ibis.literal(1)).mutate(
        idx=ibis.row_number().over(order_by=_.one, rows=(None, 0))
    )

    expr = t.distinct(on=on, keep=None).order_by(ibis.asc("idx"))
    result = expr.execute()
    df = t.execute()
    expected = (
        df.drop_duplicates(subset=on, keep=False)
        .sort_values(by=["idx"])
        .reset_index(drop=True)
    )
    assert len(result) == len(expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_hash_consistent(alltypes):
    h1 = alltypes.string_col.hash().execute(limit=10)
    h2 = alltypes.string_col.hash().execute(limit=10)
    tm.assert_series_equal(h1, h2)
    assert h1.dtype in ("i8", "uint64")


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
@pytest.mark.parametrize(
    ("from_val", "to_type", "expected"),
    [
        param(0, "float", 0.0),
        param(0.0, "int", 0),
        param("0", "int", 0),
        param("0.0", "float", 0.0),
        param(
            "a",
            "int",
            None,
            marks=pytest.mark.notyet(["polars"], reason="polars casts to nan"),
        ),
        param(
            datetime.datetime(2023, 1, 1),
            "int",
            None,
            marks=[
                pytest.mark.notyet(
                    ["clickhouse"], reason="clickhouse casts this to 1686156304"
                ),
                pytest.mark.notyet(["trino"], reason="trino raises a TrinoUserError"),
                pytest.mark.notyet(
                    ["polars"], reason="polars casts this to 1686157562300325000"
                ),
            ],
        ),
    ],
)
def test_try_cast_expected(con, from_val, to_type, expected):
    assert con.execute(ibis.literal(from_val).try_cast(to_type)) == expected


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_try_cast_table(con):
    df = pd.DataFrame({"a": ["1", "2", None], "b": ["1.0", "2.2", "goodbye"]})

    expected = pd.DataFrame({"a": [1.0, 2.0, None], "b": [1.0, 2.2, None]})

    t = ibis.memtable(df)

    tm.assert_frame_equal(con.execute(t.try_cast({"a": "int", "b": "float"})), expected)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
@pytest.mark.parametrize(
    ("from_val", "to_type", "func"),
    [
        param("a", "float", np.isnan),
        param(
            datetime.datetime(2023, 1, 1),
            "float",
            np.isnan,
            marks=[
                pytest.mark.notyet(
                    ["clickhouse"], reason="clickhouse casts this to to a number"
                ),
                pytest.mark.notyet(["trino"], reason="trino raises a TrinoUserError"),
                pytest.mark.notyet(["polars"], reason="polars casts this to a number"),
            ],
        ),
    ],
)
def test_try_cast_func(con, from_val, to_type, func):
    assert func(con.execute(ibis.literal(from_val).try_cast(to_type)))


@pytest.mark.parametrize(
    ("slc", "expected_count_fn"),
    [
        ###################
        ### NONE/ZERO start
        # no stop
        param(slice(None, 0), lambda _: 0, id="[:0]"),
        param(slice(None, None), lambda t: t.count().to_pandas(), id="[:]"),
        param(slice(0, 0), lambda _: 0, id="[0:0]"),
        param(slice(0, None), lambda t: t.count().to_pandas(), id="[0:]"),
        # positive stop
        param(slice(None, 2), lambda _: 2, id="[:2]"),
        param(slice(0, 2), lambda _: 2, id="[0:2]"),
        ##################
        ### NEGATIVE start
        # zero stop
        param(slice(-3, 0), lambda _: 0, id="[-3:0]"),
        # negative stop
        param(slice(-3, -3), lambda _: 0, id="[-3:-3]"),
        param(slice(-3, -4), lambda _: 0, id="[-3:-4]"),
        param(slice(-3, -5), lambda _: 0, id="[-3:-5]"),
        ##################
        ### POSITIVE start
        # no stop
        param(slice(3, 0), lambda _: 0, id="[3:0]"),
        param(
            slice(3, None),
            lambda t: t.count().to_pandas() - 3,
            id="[3:]",
            marks=[
                pytest.mark.notimpl(
                    raises=NotImplementedError,
                    reason="no support for offset yet",
                ),
            ],
        ),
        # positive stop
        param(slice(3, 2), lambda _: 0, id="[3:2]"),
        param(
            slice(3, 4),
            lambda _: 1,
            id="[3:4]",
            marks=[
                pytest.mark.notimpl(
                    raises=NotImplementedError,
                    reason="no support for offset yet",
                ),
            ],
        ),
    ],
)
def test_static_table_slice(slc, expected_count_fn, functional_alltypes):
    t = functional_alltypes

    rows = t[slc]
    count = rows.count().to_pandas()

    expected_count = expected_count_fn(t)
    assert count == expected_count


@pytest.mark.parametrize(
    ("slc", "expected_count_fn"),
    [
        ### NONE/ZERO start
        # negative stop
        param(slice(None, -2), lambda t: t.count().to_pandas() - 2, id="[:-2]"),
        param(slice(0, -2), lambda t: t.count().to_pandas() - 2, id="[0:-2]"),
        # no stop
        param(slice(-3, None), lambda _: 3, id="[-3:]"),
        ##################
        ### NEGATIVE start
        # negative stop
        param(slice(-3, -2), lambda _: 1, id="[-3:-2]"),
        # positive stop
        param(slice(-4000, 7000), lambda _: 3700, id="[-4000:7000]"),
        param(slice(-3, 2), lambda _: 0, id="[-3:2]"),
        ##################
        ### POSITIVE start
        # negative stop
        param(slice(3, -2), lambda t: t.count().to_pandas() - 5, id="[3:-2]"),
        param(slice(3, -4), lambda t: t.count().to_pandas() - 7, id="[3:-4]"),
    ],
    ids=str,
)
@pytest.mark.notimpl(
    reason="datafusion doesn't support dynamic limit/offset",
    raises=NotImplementedError,
)
def test_dynamic_table_slice(slc, expected_count_fn, functional_alltypes):
    rows = functional_alltypes[slc]
    count = rows.count().to_pandas()

    expected_count = expected_count_fn(functional_alltypes)
    assert count == expected_count


@pytest.mark.notimpl(
    reason="datafusion doesn't support dynamic limit/offset",
    raises=NotImplementedError,
)
def test_dynamic_table_slice_with_computed_offset(functional_alltypes):
    col = "id"
    df = functional_alltypes[[col]].to_pandas()

    assert len(df) == df[col].nunique()

    n = 10

    expr = functional_alltypes[[col]].order_by(col)[-n:]

    expected = df.sort_values([col]).iloc[-n:].reset_index(drop=True)
    result = expr.to_pandas()

    assert_frame_equal(result, expected)
