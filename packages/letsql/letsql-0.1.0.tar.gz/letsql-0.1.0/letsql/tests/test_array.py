from __future__ import annotations

import functools

import numpy as np
import pandas as pd
import pandas.testing as tm
import pytest
from pytest import param

import letsql._vendor.ibis as ibis
import letsql._vendor.ibis.common.exceptions as com
import letsql._vendor.ibis.expr.datatypes as dt
import letsql._vendor.ibis.expr.types as ir
from letsql.tests.base import assert_series_equal, assert_frame_equal


# NB: We don't check whether results are numpy arrays or lists because this
# varies across backends. At some point, we should unify the result type to be
# list.


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_array_column(alltypes, df):
    expr = ibis.array([alltypes["double_col"], alltypes["double_col"]])
    assert isinstance(expr, ir.ArrayColumn)

    result = expr.execute()
    expected = df.apply(
        lambda row: [row["double_col"], row["double_col"]],
        axis=1,
    )
    assert_series_equal(result, expected, check_names=False)


def test_array_scalar(con):
    expr = ibis.array([1.0, 2.0, 3.0])
    assert isinstance(expr, ir.ArrayScalar)

    result = con.execute(expr.name("tmp"))
    expected = np.array([1.0, 2.0, 3.0])

    assert np.array_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_array_repeat(con):
    expr = ibis.array([1.0, 2.0]) * 2

    result = con.execute(expr.name("tmp"))
    expected = np.array([1.0, 2.0, 1.0, 2.0])

    assert np.array_equal(result, expected)


# Issues #2370
@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_array_concat(con):
    left = ibis.literal([1, 2, 3])
    right = ibis.literal([2, 1])
    expr = left + right
    result = con.execute(expr.name("tmp"))
    expected = np.array([1, 2, 3, 2, 1])
    assert np.array_equal(result, expected)


# Issues #2370
@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_array_concat_variadic(con):
    left = ibis.literal([1, 2, 3])
    right = ibis.literal([2, 1])
    expr = left.concat(right, right, right)
    result = con.execute(expr.name("tmp"))
    expected = np.array([1, 2, 3, 2, 1, 2, 1, 2, 1])
    assert np.array_equal(result, expected)


# Issues #2370
@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_array_concat_some_empty(con):
    left = ibis.literal([])
    right = ibis.literal([2, 1])
    expr = left.concat(right)
    result = con.execute(expr.name("tmp"))
    expected = np.array([2, 1])
    assert np.array_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_array_radd_concat(con):
    left = [1]
    right = ibis.literal([2])
    expr = left + right
    result = con.execute(expr.name("tmp"))
    expected = np.array([1, 2])

    assert np.array_equal(result, expected)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_array_length(con):
    expr = ibis.literal([1, 2, 3]).length()
    assert con.execute(expr.name("tmp")) == 3


def test_list_literal(con):
    arr = [1, 2, 3]
    expr = ibis.literal(arr)
    result = con.execute(expr.name("tmp"))

    assert np.array_equal(result, arr)


def test_np_array_literal(con):
    arr = np.array([1, 2, 3])
    expr = ibis.literal(arr)
    result = con.execute(expr.name("tmp"))

    assert np.array_equal(result, arr)


@pytest.mark.parametrize("idx", range(3))
@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_array_index(con, idx):
    arr = [1, 2, 3]
    expr = ibis.literal(arr)
    expr = expr[idx]
    result = con.execute(expr)
    assert result == arr[idx]


@pytest.mark.notimpl(raises=Exception)
def test_array_discovery_postgres(array_types):
    t = array_types
    expected = ibis.schema(
        dict(
            x=dt.Array(dt.int64),
            y=dt.Array(dt.string),
            z=dt.Array(dt.float64),
            grouper=dt.string,
            scalar_column=dt.float64,
            multi_dim=dt.Array(dt.int64),
        )
    )
    assert t.schema() == expected


def test_array_discovery_desired(array_types):
    t = array_types
    expected = ibis.schema(
        dict(
            x=dt.Array(dt.int64),
            y=dt.Array(dt.string),
            z=dt.Array(dt.float64),
            grouper=dt.string,
            scalar_column=dt.float64,
            multi_dim=dt.Array(dt.Array(dt.int64)),
        )
    )
    assert t.schema() == expected


@pytest.mark.notimpl(raises=Exception)
def test_unnest_simple(array_types):
    array_types = array_types
    expected = (
        array_types.execute()
        .x.explode()
        .reset_index(drop=True)
        .astype("Float64")
        .rename("tmp")
    )
    expr = array_types.x.cast("!array<float64>").unnest()
    result = expr.execute().astype("Float64").rename("tmp")
    tm.assert_series_equal(result, expected)


@pytest.mark.notimpl(raises=Exception)
def test_unnest_complex(array_types):
    array_types = array_types
    df = array_types.execute()
    expr = (
        array_types.select(["grouper", "x"])
        .mutate(x=lambda t: t.x.unnest())
        .group_by("grouper")
        .aggregate(count_flat=lambda t: t.x.count())
        .order_by("grouper")
    )
    expected = (
        df[["grouper", "x"]]
        .explode("x")
        .groupby("grouper")
        .x.count()
        .rename("count_flat")
        .reset_index()
        .sort_values("grouper")
        .reset_index(drop=True)
    )
    result = expr.execute()
    tm.assert_frame_equal(result, expected)


@pytest.mark.notimpl(raises=Exception)
def test_unnest_idempotent(array_types):
    array_types = array_types
    df = array_types.execute()
    expr = (
        array_types.select(
            ["scalar_column", array_types.x.cast("!array<int64>").unnest().name("x")]
        )
        .group_by("scalar_column")
        .aggregate(x=lambda t: t.x.collect())
        .order_by("scalar_column")
    )
    result = expr.execute()
    expected = (
        df[["scalar_column", "x"]].sort_values("scalar_column").reset_index(drop=True)
    )
    tm.assert_frame_equal(result, expected)


@pytest.mark.notimpl(raises=Exception)
def test_unnest_no_nulls(array_types):
    array_types = array_types
    df = array_types.execute()
    expr = (
        array_types.select(
            ["scalar_column", array_types.x.cast("!array<int64>").unnest().name("y")]
        )
        .filter(lambda t: t.y.notnull())
        .group_by("scalar_column")
        .aggregate(x=lambda t: t.y.collect())
        .order_by("scalar_column")
    )
    result = expr.execute()
    expected = (
        df[["scalar_column", "x"]]
        .explode("x")
        .dropna(subset=["x"])
        .groupby("scalar_column")
        .x.apply(lambda xs: [x for x in xs if x is not None])
        .reset_index()
    )
    tm.assert_frame_equal(result, expected)


@pytest.mark.notimpl(raises=Exception)
def test_unnest_default_name(array_types):
    array_types = array_types
    df = array_types.execute()
    expr = (
        array_types.x.cast("!array<int64>") + ibis.array([1], type="!array<int64>")
    ).unnest()
    assert expr.get_name().startswith("ArrayConcat(")

    result = expr.name("x").execute()
    expected = df.x.map(lambda x: x + [1]).explode("x")
    tm.assert_series_equal(
        result.astype(object).fillna(pd.NA), expected.fillna(pd.NA), check_dtype=False
    )


@pytest.mark.parametrize(
    ("start", "stop"),
    [
        (1, 3),
        (1, 1),
        (2, 3),
        (2, 5),
        (None, 3),
        (None, None),
        (3, None),
        (-3, None),
        (None, -3),
        (-3, -1),
    ],
)
@pytest.mark.notimpl(raises=Exception, reason="array_types table isn't defined")
def test_array_slice(start, stop, array_types):
    expr = array_types.select(sliced=array_types.y[start:stop])
    result = expr.execute()
    expected = pd.DataFrame(
        {"sliced": array_types.y.execute().map(lambda x: x[start:stop])}
    )
    tm.assert_frame_equal(result, expected)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
@pytest.mark.parametrize(
    ("input", "output"),
    [
        param(
            {"a": [[1, None, 2], [4]]},
            {"a": [[2, None, 3], [5]]},
            id="nulls",
        ),
        param({"a": [[1, 2], [4]]}, {"a": [[2, 3], [5]]}, id="no_nulls"),
    ],
)
def test_array_map(con, input, output):
    t = ibis.memtable(input, schema=ibis.schema(dict(a="!array<int8>")))
    expected = pd.DataFrame(output)

    expr = t.select(a=t.a.map(lambda x: x + 1))
    result = con.execute(expr)
    assert_frame_equal(result, expected)

    expr = t.select(a=t.a.map(functools.partial(lambda x, y: x + y, y=1)))
    result = con.execute(expr)
    assert_frame_equal(result, expected)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
@pytest.mark.parametrize(
    ("input", "output"),
    [
        param({"a": [[1, None, 2], [4]]}, {"a": [[2], [4]]}, id="nulls"),
        param({"a": [[1, 2], [4]]}, {"a": [[2], [4]]}, id="no_nulls"),
    ],
)
def test_array_filter(con, input, output):
    t = ibis.memtable(input, schema=ibis.schema(dict(a="!array<int8>")))
    expected = pd.DataFrame(output)

    expr = t.select(a=t.a.filter(lambda x: x > 1))
    result = con.execute(expr)
    assert_frame_equal(result, expected)

    expr = t.select(a=t.a.filter(functools.partial(lambda x, y: x > y, y=1)))
    result = con.execute(expr)
    assert_frame_equal(result, expected)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_array_contains(con, array_types):
    t = array_types
    expr = t.x.contains(1)
    result = con.execute(expr)
    expected = t.x.execute().map(lambda lst: 1 in lst)
    assert_series_equal(result, expected, check_names=False)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_array_position(con):
    t = ibis.memtable({"a": [[1], [], [42, 42], []]})
    expr = t.a.index(42)
    result = con.execute(expr)
    expected = pd.Series([-1, -1, 0, -1], dtype="object")
    assert_series_equal(result, expected, check_names=False, check_dtype=False)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_array_remove(con):
    t = ibis.memtable({"a": [[3, 2], [], [42, 2], [2, 2], []]})
    expr = t.a.remove(2)
    result = con.execute(expr)
    expected = pd.Series([[3], [], [42], [], []], dtype="object")
    assert_series_equal(result, expected, check_names=False)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
@pytest.mark.parametrize(
    ("input", "expected"),
    [
        param(
            {"a": [[1, 3, 3], [], [42, 42], [], [None], None]},
            [{3, 1}, set(), {42}, set(), {None}, None],
            id="null",
        ),
        param(
            {"a": [[1, 3, 3], [], [42, 42], [], None]},
            [{3, 1}, set(), {42}, set(), None],
            id="not_null",
        ),
    ],
)
def test_array_unique(con, input, expected):
    t = ibis.memtable(input)
    expr = t.a.unique()
    result = con.execute(expr).map(set, na_action="ignore")
    expected = pd.Series(expected, dtype="object")
    assert_series_equal(result, expected, check_names=False)


@pytest.mark.notimpl(raises=Exception)
def test_array_sort(con):
    t = ibis.memtable({"a": [[3, 2], [], [42, 42], []]})
    expr = t.a.sort()
    result = con.execute(expr)
    expected = pd.Series([[2, 3], [], [42, 42], []], dtype="object")
    assert_series_equal(result, expected, check_names=False)


@pytest.mark.notimpl(raises=Exception)
def test_array_union(con):
    t = ibis.memtable({"a": [[3, 2], [], []], "b": [[1, 3], [None], [5]]})
    expr = t.a.union(t.b)
    result = con.execute(expr).map(set, na_action="ignore")
    expected = pd.Series([{1, 2, 3}, {None}, {5}], dtype="object")
    assert len(result) == len(expected)

    for i, (lhs, rhs) in enumerate(zip(result, expected)):
        assert lhs == rhs, f"row {i:d} differs"


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_array_intersect(con):
    t = ibis.memtable(
        {"a": [[3, 2], [], []], "b": [[1, 3], [None], [5]], "c": range(3)}
    )
    expr = t.select("c", d=t.a.intersect(t.b)).order_by("c").drop("c").d
    result = con.execute(expr).map(set, na_action="ignore")
    expected = pd.Series([{3}, set(), set()], dtype="object")
    assert len(result) == len(expected)

    for i, (lhs, rhs) in enumerate(zip(result, expected)):
        assert lhs == rhs, f"row {i:d} differs"


@pytest.mark.notimpl(raises=Exception)
def test_unnest_struct(con):
    data = {"value": [[{"a": 1}, {"a": 2}], [{"a": 3}, {"a": 4}]]}
    t = ibis.memtable(data, schema=ibis.schema({"value": "!array<!struct<a: !int>>"}))
    expr = t.value.unnest()

    result = con.execute(expr)

    expected = pd.DataFrame(data).explode("value").iloc[:, 0].reset_index(drop=True)
    tm.assert_series_equal(result, expected)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_zip(array_types):
    t = array_types

    x = t.x.execute()
    res = t.x.zip(t.x)
    assert res.type().value_type.names == ("f1", "f2")
    s = res.execute()
    assert len(s[0][0]) == len(res.type().value_type)
    assert len(x[0]) == len(s[0])

    x = t.x.execute()
    res = t.x.zip(t.x, t.x, t.x, t.x, t.x)
    assert res.type().value_type.names == ("f1", "f2", "f3", "f4", "f5", "f6")
    s = res.execute()
    assert len(s[0][0]) == len(res.type().value_type)
    assert len(x[0]) == len(s[0])


@pytest.mark.notimpl(raises=Exception)
def test_array_of_struct_unnest(con):
    jobs = ibis.memtable(
        {
            "steps": [
                [
                    {"status": "success"},
                    {"status": "success"},
                    {"status": None},
                    {"status": "failure"},
                ],
                [
                    {"status": None},
                    {"status": "success"},
                ],
            ]
        },
        schema=dict(steps="array<struct<status: string>>"),
    )
    expr = jobs.limit(1).steps.unnest().status
    res = con.execute(expr)
    value = res.iat[0]
    # `value` can be `None` because the order of results is arbitrary; observed
    # in the wild with the trino backend
    assert value is None or isinstance(value, str)
