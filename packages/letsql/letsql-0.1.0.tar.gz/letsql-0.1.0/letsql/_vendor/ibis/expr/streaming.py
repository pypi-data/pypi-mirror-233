from __future__ import annotations

import letsql._vendor.ibis.expr.types as ir  # noqa: TCH001
from letsql._vendor.ibis.common.grounds import Concrete


class Watermark(Concrete):
    time_col: str
    allowed_delay: ir.IntervalScalar
