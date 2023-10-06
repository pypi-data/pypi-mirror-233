from __future__ import annotations

from public import public

import letsql._vendor.ibis.expr.datatypes as dt
import letsql._vendor.ibis.expr.rules as rlz
from letsql._vendor.ibis.common.annotations import ValidationError, attribute
from letsql._vendor.ibis.common.typing import VarTuple  # noqa: TCH001
from letsql._vendor.ibis.expr.operations.core import Value


@public
class StructField(Value):
    arg: Value[dt.Struct]
    field: str

    shape = rlz.shape_like("arg")

    @attribute
    def dtype(self) -> dt.DataType:
        struct_dtype = self.arg.dtype
        value_dtype = struct_dtype[self.field]
        return value_dtype

    @property
    def name(self) -> str:
        return self.field


@public
class StructColumn(Value):
    names: VarTuple[str]
    values: VarTuple[Value]

    shape = rlz.shape_like("values")

    def __init__(self, names, values):
        if len(names) != len(values):
            raise ValidationError(
                f"Length of names ({len(names)}) does not match length of "
                f"values ({len(values)})"
            )
        super().__init__(names=names, values=values)

    @attribute
    def dtype(self) -> dt.DataType:
        dtypes = (value.dtype for value in self.values)
        return dt.Struct.from_tuples(zip(self.names, dtypes))
