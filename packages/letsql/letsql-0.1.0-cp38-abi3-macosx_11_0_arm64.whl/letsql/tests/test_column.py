from __future__ import annotations

import pytest

import letsql._vendor.ibis.common.exceptions as com


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_rowid(diamonds):
    result = diamonds.rowid().execute()
    # Only guarantee is that the values are unique integers
    assert result.is_unique

    # Can be named
    result = diamonds.rowid().name("myrowid").execute()
    assert result.is_unique
    assert result.name == "myrowid"


@pytest.mark.parametrize(
    "column",
    ["string_col", "double_col", "date_string_col", "timestamp_col"],
)
@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_distinct_column(alltypes, df, column):
    expr = alltypes[[column]].distinct()
    result = expr.execute()
    expected = df[[column]].drop_duplicates()
    assert set(result) == set(expected)
