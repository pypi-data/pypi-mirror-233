from __future__ import annotations

import contextlib
import datetime
import operator
import warnings
from operator import methodcaller

import numpy as np
import pandas as pd
import pandas.testing as tm
import pytest
from pytest import param

import letsql._vendor.ibis as ibis
import letsql._vendor.ibis.common.exceptions as com
import letsql._vendor.ibis.expr.datatypes as dt
from letsql._vendor.ibis.common.annotations import ValidationError
from letsql.tests.base import (
    default_series_rename,
    assert_series_equal,
    assert_frame_equal,
    returned_timestamp_unit,
)

try:
    from pyarrow import ArrowInvalid
except ImportError:
    ArrowInvalid = None


@pytest.mark.parametrize("attr", ["year", "month", "day"])
@pytest.mark.parametrize(
    "expr_fn",
    [
        param(lambda c: c.date(), id="date"),
        param(
            lambda c: c.cast("date"),
            id="cast",
        ),
    ],
)
def test_date_extract(alltypes, df, attr, expr_fn):
    expr = getattr(expr_fn(alltypes.timestamp_col), attr)()
    expected = getattr(df.timestamp_col.dt, attr).astype("int32")

    result = expr.name(attr).execute()

    assert_series_equal(result, expected.rename(attr))


@pytest.mark.parametrize(
    "attr",
    [
        "year",
        "month",
        "day",
        "day_of_year",
        "quarter",
        "hour",
        "minute",
        "second",
    ],
)
def test_timestamp_extract(alltypes, df, attr):
    method = getattr(alltypes.timestamp_col, attr)
    expr = method().name(attr)
    result = expr.execute()
    expected = default_series_rename(
        getattr(df.timestamp_col.dt, attr.replace("_", "")).astype("int32")
    ).rename(attr)
    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    ("func", "expected"),
    [
        param(
            methodcaller("year"),
            2015,
            id="year",
        ),
        param(
            methodcaller("month"),
            9,
            id="month",
        ),
        param(
            methodcaller("day"),
            1,
            id="day",
        ),
        param(
            methodcaller("hour"),
            14,
            id="hour",
        ),
        param(
            methodcaller("minute"),
            48,
            id="minute",
        ),
        param(
            methodcaller("second"),
            5,
            id="second",
        ),
        param(
            methodcaller("millisecond"),
            359,
            id="millisecond",
        ),
        param(
            lambda x: x.day_of_week.index(),
            1,
            id="day_of_week_index",
        ),
        param(
            lambda x: x.day_of_week.full_name(),
            "Tuesday",
            id="day_of_week_full_name",
        ),
    ],
)
def test_timestamp_extract_literal(con, func, expected):
    value = ibis.timestamp("2015-09-01 14:48:05.359")
    assert con.execute(func(value).name("tmp")) == expected


def test_timestamp_extract_microseconds(alltypes, df):
    expr = alltypes.timestamp_col.microsecond().name("microsecond")
    result = expr.execute()
    expected = default_series_rename(
        (df.timestamp_col.dt.microsecond).astype("int32")
    ).rename("microsecond")
    assert_series_equal(result, expected)


def test_timestamp_extract_milliseconds(alltypes, df):
    expr = alltypes.timestamp_col.millisecond().name("millisecond")
    result = expr.execute()
    expected = default_series_rename(
        (df.timestamp_col.dt.microsecond // 1_000).astype("int32")
    ).rename("millisecond")
    assert_series_equal(result, expected)


def test_timestamp_extract_epoch_seconds(alltypes, df):
    expr = alltypes.timestamp_col.epoch_seconds().name("tmp")
    result = expr.execute()

    expected = default_series_rename(
        (df.timestamp_col.view("int64") // 1_000_000_000).astype("int32")
    )
    assert_series_equal(result, expected)


def test_timestamp_extract_week_of_year(alltypes, df):
    expr = alltypes.timestamp_col.week_of_year().name("tmp")
    result = expr.execute()
    expected = default_series_rename(
        df.timestamp_col.dt.isocalendar().week.astype("int32")
    )
    assert_series_equal(result, expected)


PANDAS_UNITS = {
    "m": "Min",
    "ms": "L",
}


@pytest.mark.parametrize(
    "unit",
    [
        param(
            "Y",
        ),
        param(
            "M",
        ),
        param(
            "D",
        ),
        param(
            "W",
        ),
        param(
            "h",
        ),
        param(
            "m",
        ),
        param(
            "s",
        ),
        param(
            "ms",
        ),
        param(
            "us",
        ),
        param(
            "ns",
        ),
    ],
)
@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_timestamp_truncate(alltypes, df, unit):
    expr = alltypes.timestamp_col.truncate(unit).name("tmp")

    unit = PANDAS_UNITS.get(unit, unit)

    try:
        expected = df.timestamp_col.dt.floor(unit)
    except ValueError:
        expected = df.timestamp_col.dt.to_period(unit).dt.to_timestamp()

    result = expr.execute()
    expected = default_series_rename(expected)

    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    "unit",
    [
        "Y",
        "M",
        "D",
        param(
            "W",
        ),
    ],
)
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_date_truncate(alltypes, df, unit):
    expr = alltypes.timestamp_col.date().truncate(unit).name("tmp")

    unit = PANDAS_UNITS.get(unit, unit)

    try:
        expected = df.timestamp_col.dt.floor(unit)
    except ValueError:
        expected = df.timestamp_col.dt.to_period(unit).dt.to_timestamp()

    result = expr.execute()
    expected = default_series_rename(expected)

    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    ("unit", "displacement_type"),
    [
        param(
            "Y",
            pd.offsets.DateOffset,
            # TODO - DateOffset - #2553
        ),
        param("Q", pd.offsets.DateOffset, marks=pytest.mark.xfail),
        param(
            "M",
            pd.offsets.DateOffset,
            # TODO - DateOffset - #2553
        ),
        param(
            "W",
            pd.offsets.DateOffset,
            # TODO - DateOffset - #2553
        ),
        param(
            "D",
            pd.offsets.DateOffset,
        ),
        param(
            "h",
            pd.Timedelta,
        ),
        param(
            "m",
            pd.Timedelta,
        ),
        param(
            "s",
            pd.Timedelta,
        ),
        param(
            "ms",
            pd.Timedelta,
        ),
        param(
            "us",
            pd.Timedelta,
        ),
    ],
)
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_integer_to_interval_timestamp(con, alltypes, df, unit, displacement_type):
    interval = alltypes.int_col.to_interval(unit=unit)
    expr = (alltypes.timestamp_col + interval).name("tmp")

    def convert_to_offset(offset, displacement_type=displacement_type):
        resolution = f"{interval.op().dtype.resolution}s"
        return displacement_type(**{resolution: offset})

    with warnings.catch_warnings():
        # both the implementation and test code raises pandas
        # PerformanceWarning, because We use DateOffset addition
        warnings.simplefilter("ignore", category=pd.errors.PerformanceWarning)
        result = con.execute(expr)
        offset = df.int_col.apply(convert_to_offset)
        expected = df.timestamp_col + offset

    expected = default_series_rename(expected)
    assert_series_equal(result, expected.astype("datetime64[ns]"))


@pytest.mark.parametrize(
    "unit", ["Y", param("Q", marks=pytest.mark.xfail), "M", "W", "D"]
)
# TODO - DateOffset - #2553
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_integer_to_interval_date(con, alltypes, df, unit):
    interval = alltypes.int_col.to_interval(unit=unit)
    array = alltypes.date_string_col.split("/")
    month, day, year = array[0], array[1], array[2]
    date_col = expr = ibis.literal("-").join(["20" + year, month, day]).cast("date")
    expr = (date_col + interval).name("tmp")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=pd.errors.PerformanceWarning)
        result = con.execute(expr)

    def convert_to_offset(x):
        resolution = f"{interval.type().resolution}s"
        return pd.offsets.DateOffset(**{resolution: x})

    offset = df.int_col.apply(convert_to_offset)
    with warnings.catch_warnings():
        warnings.simplefilter(
            "ignore", category=(UserWarning, pd.errors.PerformanceWarning)
        )
        expected = pd.to_datetime(df.date_string_col) + offset

    expected = default_series_rename(expected)
    assert_series_equal(result, expected.map(lambda ts: ts.normalize()))


date_value = pd.Timestamp("2017-12-31")
timestamp_value = pd.Timestamp("2018-01-01 18:18:18")


@pytest.mark.parametrize(
    ("expr_fn", "expected_fn"),
    [
        param(
            lambda t: t.timestamp_col + ibis.interval(days=4),
            lambda t: t.timestamp_col + pd.Timedelta(days=4),
            id="timestamp-add-interval",
            marks=[
                pytest.mark.notimpl(
                    ["sqlite"],
                    raises=com.OperationNotDefinedError,
                ),
                pytest.mark.notimpl(
                    ["druid"],
                    raises=ValidationError,
                    reason="Given argument with datatype interval('D') is not implicitly castable to string",
                ),
            ],
        ),
        param(
            lambda t: t.timestamp_col + (ibis.interval(days=4) - ibis.interval(days=2)),
            lambda t: t.timestamp_col + (pd.Timedelta(days=4) - pd.Timedelta(days=2)),
            id="timestamp-add-interval-binop",
        ),
        param(
            lambda t: t.timestamp_col
            + (ibis.interval(days=4) + ibis.interval(hours=2)),
            lambda t: t.timestamp_col + (pd.Timedelta(days=4) + pd.Timedelta(hours=2)),
            id="timestamp-add-interval-binop-different-units",
        ),
        param(
            lambda t: t.timestamp_col - ibis.interval(days=17),
            lambda t: t.timestamp_col - pd.Timedelta(days=17),
            id="timestamp-subtract-interval",
        ),
        param(
            lambda t: t.timestamp_col.date() + ibis.interval(days=4),
            lambda t: t.timestamp_col.dt.floor("d") + pd.Timedelta(days=4),
            id="date-add-interval",
        ),
        param(
            lambda t: t.timestamp_col.date() - ibis.interval(days=14),
            lambda t: t.timestamp_col.dt.floor("d") - pd.Timedelta(days=14),
            id="date-subtract-interval",
        ),
        param(
            lambda t: t.timestamp_col - ibis.timestamp(timestamp_value),
            lambda t: pd.Series(
                t.timestamp_col.sub(timestamp_value).values.astype("timedelta64[s]")
            ).dt.floor("s"),
            id="timestamp-subtract-timestamp",
        ),
        param(
            lambda t: t.timestamp_col.date() - ibis.date(date_value),
            lambda t: pd.Series(
                (t.timestamp_col.dt.floor("d") - date_value).values.astype(
                    "timedelta64[D]"
                )
            ),
            id="date-subtract-date",
        ),
    ],
)
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_temporal_binop(con, alltypes, df, expr_fn, expected_fn):
    expr = expr_fn(alltypes).name("tmp")
    expected = expected_fn(df)

    result = con.execute(expr)
    expected = default_series_rename(expected)

    assert_series_equal(result, expected)


def plus(t, td):
    return t.timestamp_col + pd.Timedelta(td)


def minus(t, td):
    return t.timestamp_col - pd.Timedelta(td)


@pytest.mark.parametrize(
    ("timedelta", "temporal_fn"),
    [
        param(
            "36500d",
            plus,
        ),
        param(
            "5W",
            plus,
        ),
        param(
            "3d",
            plus,
        ),
        param(
            "2h",
            plus,
        ),
        param(
            "3m",
            plus,
        ),
        param(
            "10s",
            plus,
        ),
        param(
            "36500d",
            minus,
        ),
        param(
            "5W",
            minus,
        ),
        param(
            "3d",
            minus,
        ),
        param(
            "2h",
            minus,
        ),
        param(
            "3m",
            minus,
        ),
        param(
            "10s",
            minus,
        ),
    ],
)
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_temporal_binop_pandas_timedelta(con, alltypes, df, timedelta, temporal_fn):
    expr = temporal_fn(alltypes, timedelta).name("tmp")
    expected = temporal_fn(df, timedelta)

    result = con.execute(expr)
    expected = default_series_rename(expected)

    assert_series_equal(result, expected)


@pytest.mark.parametrize("func_name", ["gt", "ge", "lt", "le", "eq", "ne"])
def test_timestamp_comparison_filter(con, alltypes, df, func_name):
    ts = pd.Timestamp("20100302", tz="UTC").to_pydatetime()

    comparison_fn = getattr(operator, func_name)
    expr = alltypes.filter(
        comparison_fn(alltypes.timestamp_col.cast("timestamp('UTC')"), ts)
    )

    col = df.timestamp_col.dt.tz_localize("UTC")
    expected = df[comparison_fn(col, ts)]
    result = con.execute(expr)

    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "func_name",
    [
        param(
            "gt",
        ),
        param(
            "ge",
        ),
        param(
            "lt",
        ),
        param(
            "le",
        ),
        "eq",
        "ne",
    ],
)
def test_timestamp_comparison_filter_numpy(con, alltypes, df, func_name):
    ts = np.datetime64("2010-03-02 00:00:00.000123")

    comparison_fn = getattr(operator, func_name)
    expr = alltypes.filter(
        comparison_fn(alltypes.timestamp_col.cast("timestamp('UTC')"), ts)
    )

    ts = pd.Timestamp(ts.item(), tz="UTC")

    col = df.timestamp_col.dt.tz_localize("UTC")
    expected = df[comparison_fn(col, ts)]
    result = con.execute(expr)

    assert_frame_equal(result, expected)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_interval_add_cast_scalar(alltypes):
    timestamp_date = alltypes.timestamp_col.date()
    delta = ibis.literal(10).cast("interval('D')")
    expr = (timestamp_date + delta).name("result")
    result = expr.execute()
    expected = timestamp_date.name("result").execute() + pd.Timedelta(10, unit="D")
    assert_series_equal(result, expected)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_interval_add_cast_column(alltypes, df):
    timestamp_date = alltypes.timestamp_col.date()
    delta = alltypes.bigint_col.cast("interval('D')")
    expr = alltypes["id", (timestamp_date + delta).name("tmp")]
    result = expr.execute().sort_values("id").reset_index().tmp
    df = df.sort_values("id").reset_index(drop=True)
    expected = (
        df["timestamp_col"]
        .dt.normalize()
        .add(df.bigint_col.astype("timedelta64[D]"))
        .rename("tmp")
    )
    assert_series_equal(result, expected)


@pytest.mark.parametrize(
    ("expr_fn", "pandas_pattern"),
    [
        param(
            lambda t: t.timestamp_col.strftime("%Y%m%d").name("formatted"),
            "%Y%m%d",
            id="literal_format_str",
        ),
        param(
            lambda t: (
                t.mutate(suffix="%d")
                .select(
                    [
                        lambda t: t.timestamp_col.strftime("%Y%m" + t.suffix).name(
                            "formatted"
                        )
                    ]
                )
                .formatted
            ),
            "%Y%m%d",
            id="column_format_str",
        ),
    ],
)
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_strftime(alltypes, df, expr_fn, pandas_pattern):
    expr = expr_fn(alltypes)
    expected = df.timestamp_col.dt.strftime(pandas_pattern).rename("formatted")

    result = expr.execute()
    assert_series_equal(result, expected)


unit_factors = {"s": 10**9, "ms": 10**6, "us": 10**3, "ns": 1}


@pytest.mark.parametrize(
    "unit",
    [
        "s",
        param(
            "ms",
        ),
        param(
            "us",
        ),
        param(
            "ns",
        ),
    ],
)
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_integer_to_timestamp(con, unit):
    backend_unit = returned_timestamp_unit
    factor = unit_factors[unit]

    pandas_ts = pd.Timestamp("2018-04-13 09:54:11.872832").floor(unit).value

    # convert the timestamp to the input unit being tested
    int_expr = ibis.literal(pandas_ts // factor)
    expr = int_expr.to_timestamp(unit).name("tmp")
    result = con.execute(expr)
    expected = pd.Timestamp(pandas_ts, unit="ns").floor(backend_unit)

    assert result == expected


@pytest.mark.parametrize(
    "fmt",
    [
        # "11/01/10" - "month/day/year"
        param(
            "%m/%d/%y",
            id="mysql_format",
        ),
        param(
            "MM/dd/yy",
            id="pyspark_format",
        ),
    ],
)
@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_string_to_timestamp(alltypes, fmt):
    table = alltypes
    result = table.mutate(date=table.date_string_col.to_timestamp(fmt)).execute()

    # TEST: do we get the same date out, that we put in?
    # format string assumes that we are using pandas' strftime
    for i, val in enumerate(result["date"]):
        assert val.strftime("%m/%d/%y") == result["date_string_col"][i]


@pytest.mark.parametrize(
    ("date", "expected_index", "expected_day"),
    [
        param("2017-01-01", 6, "Sunday", id="sunday"),
        param("2017-01-02", 0, "Monday", id="monday"),
        param("2017-01-03", 1, "Tuesday", id="tuesday"),
        param("2017-01-04", 2, "Wednesday", id="wednesday"),
        param("2017-01-05", 3, "Thursday", id="thursday"),
        param("2017-01-06", 4, "Friday", id="friday"),
        param("2017-01-07", 5, "Saturday", id="saturday"),
    ],
)
@pytest.mark.xfail_version(
    raises=Exception,
    reason="Exception: Arrow error: Cast error: Cannot cast string to value of Date64 type",
)
def test_day_of_week_scalar(con, date, expected_index, expected_day):
    expr = ibis.literal(date).cast(dt.date)
    result_index = con.execute(expr.day_of_week.index().name("tmp"))
    assert result_index == expected_index

    result_day = con.execute(expr.day_of_week.full_name().name("tmp"))
    assert result_day.lower() == expected_day.lower()


def test_day_of_week_column(alltypes, df):
    expr = alltypes.timestamp_col.day_of_week

    result_index = expr.index().name("tmp").execute()
    expected_index = df.timestamp_col.dt.dayofweek.astype("int16")

    assert_series_equal(result_index, expected_index, check_names=False)

    result_day = expr.full_name().name("tmp").execute()
    expected_day = df.timestamp_col.dt.day_name()

    assert_series_equal(result_day, expected_day, check_names=False)


@pytest.mark.parametrize(
    ("day_of_week_expr", "day_of_week_pandas"),
    [
        param(
            lambda t: t.timestamp_col.day_of_week.index().count(),
            lambda s: s.dt.dayofweek.count(),
            id="day_of_week_index",
        ),
        param(
            lambda t: t.timestamp_col.day_of_week.full_name().length().sum(),
            lambda s: s.dt.day_name().str.len().sum(),
            id="day_of_week_full_name",
        ),
    ],
)
def test_day_of_week_column_group_by(
    alltypes, df, day_of_week_expr, day_of_week_pandas
):
    expr = alltypes.group_by("string_col").aggregate(
        day_of_week_result=day_of_week_expr
    )
    schema = expr.schema()
    assert schema["day_of_week_result"] == dt.int64

    result = expr.execute().sort_values("string_col")
    expected = (
        df.groupby("string_col")
        .timestamp_col.apply(day_of_week_pandas)
        .reset_index()
        .rename(columns={"timestamp_col": "day_of_week_result"})
    )

    # FIXME(#1536): Pandas backend should use query.schema().apply_to
    assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_now(con):
    expr = ibis.now()
    result = con.execute(expr.name("tmp"))
    assert isinstance(result, datetime.datetime)


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
def test_now_from_projection(alltypes):
    n = 2
    expr = alltypes.select(now=ibis.now()).limit(n)
    result = expr.execute()
    ts = result.now
    assert len(result) == n
    assert ts.nunique() == 1
    assert ~pd.isna(ts.iat[0])


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_date_literal(con):
    expr = ibis.date(2022, 2, 4)
    result = con.execute(expr)
    assert result.strftime("%Y-%m-%d") == "2022-02-04"


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_timestamp_literal(con):
    expr = ibis.timestamp(2022, 2, 4, 16, 20, 0)
    result = con.execute(expr)
    if not isinstance(result, str):
        result = result.strftime("%Y-%m-%d %H:%M:%S%Z")
    assert result == "2022-02-04 16:20:00"


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
@pytest.mark.parametrize(
    ("timezone", "expected"),
    [
        param(
            "Europe/London",
            "2022-02-04 16:20:00GMT",
            id="name",
        ),
        param(
            "PST8PDT",
            "2022-02-04 08:20:00PST",
            # The time zone for Berkeley, California.
            id="iso",
        ),
    ],
)
def test_timestamp_with_timezone_literal(con, timezone, expected):
    expr = ibis.timestamp(2022, 2, 4, 16, 20, 0).cast(dt.Timestamp(timezone=timezone))
    result = con.execute(expr)
    if not isinstance(result, str):
        result = result.strftime("%Y-%m-%d %H:%M:%S%Z")
    assert result == expected


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_time_literal(con):
    expr = ibis.time(16, 20, 0)
    result = con.execute(expr)
    with contextlib.suppress(AttributeError):
        result = result.to_pytimedelta()
    assert str(result) == "16:20:00"


@pytest.mark.notimpl(raises=com.OperationNotDefinedError)
@pytest.mark.parametrize(
    "microsecond",
    [
        0,
        param(
            561021,
        ),
    ],
    ids=["second", "subsecond"],
)
def test_extract_time_from_timestamp(con, microsecond):
    raw_ts = datetime.datetime(2023, 1, 7, 13, 20, 5, microsecond)
    ts = ibis.timestamp(raw_ts)
    expr = ts.time()

    result = con.execute(expr)
    expected = raw_ts.time()

    assert result == expected


@pytest.mark.xfail_version(
    raises=Exception,
    reason='This feature is not implemented: Can\'t create a scalar from array of type "Duration(Second)"',
)
def test_interval_literal(con):
    expr = ibis.interval(1, unit="s")
    result = con.execute(expr)
    assert str(result) == "0 days 00:00:01"


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_date_column_from_ymd(con, alltypes, df):
    c = alltypes.timestamp_col
    expr = ibis.date(c.year(), c.month(), c.day())
    tbl = alltypes[expr.name("timestamp_col")]
    result = con.execute(tbl)

    golden = df.timestamp_col.dt.date.astype("datetime64[ns]")
    tm.assert_series_equal(golden, result.timestamp_col)


@pytest.mark.notimpl(
    raises=com.OperationNotDefinedError,
)
def test_timestamp_column_from_ymdhms(con, alltypes, df):
    c = alltypes.timestamp_col
    expr = ibis.timestamp(
        c.year(), c.month(), c.day(), c.hour(), c.minute(), c.second()
    )
    tbl = alltypes[expr.name("timestamp_col")]
    result = con.execute(tbl)

    golden = df.timestamp_col.dt.floor("s").astype("datetime64[ns]")
    tm.assert_series_equal(golden, result.timestamp_col)


@pytest.mark.xfail_version(
    raises=Exception,
    reason="Arrow error: Cast error: Cannot cast string '2022-02-24' to value of Date64 type",
)
def test_date_scalar_from_iso(con):
    expr = ibis.literal("2022-02-24")
    expr2 = ibis.date(expr)

    result = con.execute(expr2)
    assert result.strftime("%Y-%m-%d") == "2022-02-24"


@pytest.mark.xfail_version(
    raises=Exception,
    reason="Arrow error: Cast error: Cannot cast string '2010-11-13' to value of Date64 type",
)
def test_date_column_from_iso(con, alltypes, df):
    expr = (
        alltypes.year.cast("string")
        + "-"
        + alltypes.month.cast("string").lpad(2, "0")
        + "-13"
    )
    expr = ibis.date(expr)

    result = con.execute(expr.name("tmp"))
    golden = df.year.astype(str) + "-" + df.month.astype(str).str.rjust(2, "0") + "-13"
    actual = result.dt.strftime("%Y-%m-%d")
    tm.assert_series_equal(golden.rename("tmp"), actual.rename("tmp"))


def test_timestamp_extract_milliseconds_with_big_value(con):
    timestamp = ibis.timestamp("2021-01-01 01:30:59.333456")
    millis = timestamp.millisecond()
    result = con.execute(millis.name("tmp"))
    assert result == 333


@pytest.mark.notimpl(
    raises=Exception,
    reason=(
        "This feature is not implemented: Unsupported CAST from Int32 to Timestamp(Nanosecond, None)"
    ),
)
def test_integer_cast_to_timestamp_column(alltypes, df):
    expr = alltypes.int_col.cast("timestamp")
    expected = pd.to_datetime(df.int_col, unit="s").rename(expr.get_name())
    result = expr.execute()
    assert_series_equal(result, expected)


@pytest.mark.notimpl(
    raises=Exception,
    reason=(
        "Internal error: Invalid aggregate expression 'CAST(MIN(functional_alltypes.int_col) "
        "AS Timestamp(Nanosecond, None)) AS tmp'. This was likely caused by a bug in "
        "DataFusion's code and we would welcome that you file an bug report in our issue tracker"
    ),
)
def test_integer_cast_to_timestamp_scalar(alltypes, df):
    expr = alltypes.int_col.min().cast("timestamp")
    result = expr.execute()
    expected = pd.to_datetime(df.int_col.min(), unit="s")
    assert result == expected


def test_big_timestamp(con):
    # TODO: test with a timezone
    value = ibis.timestamp("2419-10-11 10:10:25")
    result = con.execute(value.name("tmp"))
    expected = datetime.datetime(2419, 10, 11, 10, 10, 25)
    assert result == expected


DATE = datetime.date(2010, 11, 1)


def build_date_col(t):
    return (
        t.year.cast("string")
        + "-"
        + t.month.cast("string").lpad(2, "0")
        + "-"
        + (t.int_col + 1).cast("string").lpad(2, "0")
    ).cast("date")


@pytest.mark.xfail_version(
    datafusion=["datafusion<31"],
    raises=Exception,
    reason="Arrow error: Cast error: Cannot cast string '2010-11-01' to value of Date64 type",
)
@pytest.mark.parametrize(
    ("left_fn", "right_fn"),
    [
        param(build_date_col, lambda _: DATE, id="column_date"),
        param(lambda _: DATE, build_date_col, id="date_column"),
    ],
)
def test_timestamp_date_comparison(alltypes, df, left_fn, right_fn):
    left = left_fn(alltypes)
    right = right_fn(alltypes)
    expr = left == right
    result = expr.name("result").execute()
    expected = (
        pd.to_datetime(
            (
                df.year.astype(str)
                .add("-")
                .add(df.month.astype(str).str.rjust(2, "0"))
                .add("-")
                .add(df.int_col.add(1).astype(str).str.rjust(2, "0"))
            ),
            format="%Y-%m-%d",
            exact=True,
        )
        .eq(pd.Timestamp(DATE))
        .rename("result")
    )
    assert_series_equal(result, expected)


def test_large_timestamp(con):
    huge_timestamp = datetime.datetime(year=4567, month=1, day=1)
    expr = ibis.timestamp("4567-01-01 00:00:00")
    result = con.execute(expr)
    assert result.replace(tzinfo=None) == huge_timestamp


@pytest.mark.parametrize(
    ("ts", "scale", "unit"),
    [
        param(
            "2023-01-07 13:20:05.561",
            3,
            "ms",
            id="ms",
        ),
        param(
            "2023-01-07 13:20:05.561021",
            6,
            "us",
            id="us",
        ),
        param(
            "2023-01-07 13:20:05.561000231",
            9,
            "ns",
            id="ns",
        ),
    ],
)
def test_timestamp_precision_output(con, ts, scale, unit):
    dtype = dt.Timestamp(scale=scale)
    expr = ibis.literal(ts).cast(dtype)
    result = con.execute(expr)
    expected = pd.Timestamp(ts).floor(unit)
    assert result == expected
