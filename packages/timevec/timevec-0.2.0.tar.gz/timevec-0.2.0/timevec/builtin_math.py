import datetime
import math
from typing import Dict, Iterable, Tuple

import timevec.util as util


def long_time_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the long time as a vector"""
    range = util.long_time_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def millennium_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the millennium as a vector"""
    range = util.millennium_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def century_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the century as a vector"""
    range = util.century_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def decade_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the decade as a vector"""
    range = util.decade_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def year_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the year as a vector"""
    range = util.year_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def month_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the month as a vector"""
    range = util.month_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def week_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the week as a vector"""
    # weekday is 0 for Monday and 6 for Sunday
    range = util.week_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def day_vec(dt: datetime.datetime) -> Tuple[float, float]:
    """Represent the elapsed time in the day as a vector"""
    range = util.day_range(dt)
    rate = range.time_elapsed_ratio(dt)
    return ratio_to_vec(rate)


def ratio_to_vec(rate: float) -> Tuple[float, float]:
    """Convert a rate to a vector"""
    s = 2 * math.pi * rate
    x = math.cos(s)
    y = math.sin(s)
    return x, y


def vec_to_ratio(x: float, y: float) -> float:
    """Convert a vector to a rate"""
    # atan2 returns a value in the range [-pi, pi]
    # so we need to convert it to the range [0, 2*pi]
    angle = math.atan2(y, x) / (2.0 * math.pi)
    return angle if angle >= 0 else angle + 1.0


def datetime_to_vecs(
    dt: datetime.datetime,
    targets: Iterable[util.TARGET],
) -> Dict[util.TARGET, Tuple[float, float]]:
    """Convert a datetime to a vector"""
    d: Dict[util.TARGET, Tuple[float, float]] = {}
    if "long_time" in targets:
        d["long_time"] = long_time_vec(dt)
    if "millennium" in targets:
        d["millennium"] = millennium_vec(dt)
    if "century" in targets:
        d["century"] = century_vec(dt)
    if "decade" in targets:
        d["decade"] = decade_vec(dt)
    if "year" in targets:
        d["year"] = year_vec(dt)
    if "month" in targets:
        d["month"] = month_vec(dt)
    if "week" in targets:
        d["week"] = week_vec(dt)
    if "day" in targets:
        d["day"] = day_vec(dt)
    return d


def datetime_from_vecs(
    items: Dict[util.TARGET, Tuple[float, float]],
) -> datetime.datetime:
    """Convert a vector to a datetime"""
    # long time → millennium → century → decade → year → month → week → day
    t = util.BEGIN_OF_DATETIME

    if "long_time" in items:
        range = util.long_time_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(*items["long_time"]))

    if "millennium" in items:
        range = util.millennium_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(*items["millennium"]))

    if "century" in items:
        range = util.century_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(*items["century"]))

    if "decade" in items:
        range = util.decade_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(*items["decade"]))

    if "year" in items:
        range = util.year_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(*items["year"]))

    if "month" in items:
        range = util.month_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(*items["month"]))

    if "week" in items:
        range = util.week_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(*items["week"]))

    if "day" in items:
        range = util.day_range(t)
        t = range.current_time_by_ratio(vec_to_ratio(*items["day"]))

    return t


__all__ = [
    "long_time_vec",
    "millennium_vec",
    "century_vec",
    "decade_vec",
    "year_vec",
    "month_vec",
    "week_vec",
    "day_vec",
    "datetime_to_vecs",
    "datetime_from_vecs",
]
