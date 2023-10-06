import datetime
from typing import Dict, Iterable

import numpy as np
import numpy.typing as npt

import timevec.numpy as tvn
import timevec.util as util


def long_time_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the long time as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = util.long_time_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return tvn.ratio_to_vec(rate, dtype=dtype)


def millennium_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the millennium as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = util.millennium_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return tvn.ratio_to_vec(rate, dtype=dtype)


def century_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the century as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = util.century_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return tvn.ratio_to_vec(rate, dtype=dtype)


def year_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the year as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = util.year_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return tvn.ratio_to_vec(rate, dtype=dtype)


def month_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the month as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = util.month_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return tvn.ratio_to_vec(rate, dtype=dtype)


def week_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the week as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = util.week_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return tvn.ratio_to_vec(rate, dtype=dtype)


def day_vec(
    dt: np.datetime64, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the day as a vector"""
    dt2 = datetime64_to_datetime(dt)
    range = util.day_range(dt2)
    rate = range.time_elapsed_ratio(dt2)
    return tvn.ratio_to_vec(rate, dtype=dtype)


def datetime64_to_datetime(dt: np.datetime64) -> datetime.datetime:
    """Convert a numpy.datetime64 to a datetime.datetime"""
    dt64 = np.datetime64(dt)
    ts = float(
        (dt64 - np.datetime64("1970-01-01T00:00:00")) / np.timedelta64(1, "s")
    )
    return datetime.datetime.utcfromtimestamp(ts)


def datetime_to_datetime64(dt: datetime.datetime) -> np.datetime64:
    """Convert a datetime.datetime to a numpy.datetime64"""
    ts = dt.timestamp()
    dt64 = np.datetime64("1970-01-01T00:00:00") + np.timedelta64(int(ts), "s")
    return dt64


def datetime64_to_vecs(
    dt: np.datetime64,
    targets: Iterable[util.TARGET],
    *,
    dtype: npt.DTypeLike = np.float64
) -> Dict[util.TARGET, npt.NDArray]:
    """Convert a numpy.datetime64 to a vector"""
    dt2 = datetime64_to_datetime(dt)
    return tvn.datetime_to_vecs(dt2, targets, dtype=dtype)


def datetime64_from_vecs(
    items: Dict[util.TARGET, npt.NDArray]
) -> np.datetime64:
    """Convert a vector to a numpy.datetime64"""
    dt = tvn.datetime_from_vecs(items)
    return datetime_to_datetime64(dt)


__all__ = [
    "century_vec",
    "day_vec",
    "long_time_vec",
    "millennium_vec",
    "month_vec",
    "week_vec",
    "year_vec",
    "datetime64_from_vecs",
    "datetime64_to_vecs",
]
