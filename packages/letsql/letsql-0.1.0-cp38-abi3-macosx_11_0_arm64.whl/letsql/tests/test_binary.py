from __future__ import annotations

import letsql._vendor.ibis as ibis


def test_binary_literal(con):
    expr = ibis.literal(b"A")
    result = con.execute(expr)
    assert result == b"A"
