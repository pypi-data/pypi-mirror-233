import datetime
from typing import Dict, Iterable

import numpy as np
import numpy.typing as npt

import timevec.util as util


def long_time_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the long time as a vector"""
    range = util.long_time_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def millennium_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the millennium as a vector"""
    range = util.millennium_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def century_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the century as a vector"""
    range = util.century_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def decade_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the decade as a vector"""
    range = util.decade_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def year_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the year as a vector"""
    range = util.year_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def month_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the month as a vector"""
    range = util.month_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def week_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the week as a vector"""
    range = util.week_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def day_vec(
    dt: datetime.datetime, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the elapsed time in the day as a vector"""
    range = util.day_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate, dtype=dtype)


def ratio_to_vec(
    ratio: float, *, dtype: npt.DTypeLike = np.float64
) -> npt.NDArray:
    """Represent the ratio as a vector"""
    vec = np.zeros(2, dtype=dtype)
    vec[0] = np.cos(2.0 * np.pi * ratio)
    vec[1] = np.sin(2.0 * np.pi * ratio)
    return vec


def vec_to_ratio(arr: npt.NDArray) -> float:
    """Convert a vector to a ratio"""
    # atan2 returns a value in the range [-pi, pi]
    # so we need to convert it to the range [0, 2*pi]
    base = np.arctan2(arr[1], arr[0]) / (2.0 * np.pi)
    return float(base if base >= 0.0 else base + 1.0)


def datetime_to_vecs(
    dt: datetime.datetime,
    targets: Iterable[util.TARGET],
    *,
    dtype: npt.DTypeLike = np.float64,
) -> Dict[util.TARGET, npt.NDArray]:
    """Convert a datetime to a vector"""
    d: Dict[util.TARGET, npt.NDArray] = {}
    if "long_time" in targets:
        d["long_time"] = long_time_vec(dt, dtype=dtype)
    if "millennium" in targets:
        d["millennium"] = millennium_vec(dt, dtype=dtype)
    if "century" in targets:
        d["century"] = century_vec(dt, dtype=dtype)
    if "decade" in targets:
        d["decade"] = decade_vec(dt, dtype=dtype)
    if "year" in targets:
        d["year"] = year_vec(dt, dtype=dtype)
    if "month" in targets:
        d["month"] = month_vec(dt, dtype=dtype)
    if "week" in targets:
        d["week"] = week_vec(dt, dtype=dtype)
    if "day" in targets:
        d["day"] = day_vec(dt, dtype=dtype)
    return d


def datetime_from_vecs(
    items: Dict[util.TARGET, npt.NDArray],
) -> datetime.datetime:
    """Convert a vector to a datetime"""
    # long time → millennium → century → decade → year → month → week → day
    t = util.BEGIN_OF_DATETIME

    if "long_time" in items:
        range = util.long_time_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(items["long_time"]))

    if "millennium" in items:
        range = util.millennium_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(items["millennium"]))

    if "century" in items:
        range = util.century_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(items["century"]))

    if "decade" in items:
        range = util.decade_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(items["decade"]))

    if "year" in items:
        range = util.year_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(items["year"]))

    if "month" in items:
        range = util.month_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(items["month"]))

    if "week" in items:
        range = util.week_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(items["week"]))

    if "day" in items:
        range = util.day_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(items["day"]))

    return t


__all__ = [
    "century_vec",
    "day_vec",
    "long_time_vec",
    "millennium_vec",
    "month_vec",
    "week_vec",
    "year_vec",
    "datetime_from_vecs",
    "datetime_to_vecs",
]
