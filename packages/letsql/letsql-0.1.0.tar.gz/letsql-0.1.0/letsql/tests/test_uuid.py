from __future__ import annotations

import uuid

import pytest
import sqlalchemy.exc
from packaging.version import parse as vparse

import letsql._vendor.ibis as ibis
import letsql._vendor.ibis.expr.datatypes as dt

RAW_TEST_UUID = "08f48812-7948-4718-96c7-27fa6a398db6"
TEST_UUID = uuid.UUID(RAW_TEST_UUID)

SQLALCHEMY2 = vparse(sqlalchemy.__version__) >= vparse("2")


@pytest.mark.notimpl(raises=NotImplementedError)
def test_uuid_literal(con):
    expr = ibis.literal(RAW_TEST_UUID, type=dt.uuid)
    result = con.execute(expr)

    assert result == TEST_UUID
