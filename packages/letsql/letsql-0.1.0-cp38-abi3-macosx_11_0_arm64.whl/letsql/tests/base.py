from __future__ import annotations

from typing import Any

import pandas as pd
from pandas import testing as tm

reduction_tolerance = 1e-7
check_dtype = True
check_names = True
returned_timestamp_unit = "ns"


def assert_frame_equal(
    left: pd.DataFrame, right: pd.DataFrame, *args: Any, **kwargs: Any
) -> None:
    left = left.reset_index(drop=True)
    right = right.reset_index(drop=True)
    kwargs.setdefault("check_dtype", check_dtype)
    tm.assert_frame_equal(left, right, *args, **kwargs)


def assert_series_equal(
    left: pd.Series, right: pd.Series, *args: Any, **kwargs: Any
) -> None:
    kwargs.setdefault("check_dtype", check_dtype)
    kwargs.setdefault("check_names", check_names)
    tm.assert_series_equal(left, right, *args, **kwargs)


def default_series_rename(series: pd.Series, name: str = "tmp") -> pd.Series:
    return series.rename(name)
