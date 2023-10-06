from __future__ import annotations

import letsql._vendor.ibis as ibis
import letsql._vendor.ibis.examples as ex
from letsql._vendor.ibis import deferred as _
from letsql._vendor.ibis import selectors as s
from letsql._vendor.ibis import udf

ibis.options.interactive = True

__all__ = ["_", "ex", "ibis", "s", "udf"]
