from __future__ import annotations

__version__ = "6.1.0"

from letsql._vendor.ibis import examples, util
from letsql._vendor.ibis.backends.base import BaseBackend
from letsql._vendor.ibis.common.exceptions import IbisError
from letsql._vendor.ibis.config import options
from letsql._vendor.ibis.expr import api
from letsql._vendor.ibis.expr import types as ir
from letsql._vendor.ibis.expr.api import *  # noqa: F403
from letsql._vendor.ibis.expr.operations import udf

__all__ = [  # noqa: PLE0604
    "api",
    "examples",
    "ir",
    "udf",
    "util",
    "BaseBackend",
    "IbisError",
    "options",
    *api.__all__,
]
