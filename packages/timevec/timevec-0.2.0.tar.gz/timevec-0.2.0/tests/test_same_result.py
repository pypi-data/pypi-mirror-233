# Test if the function implemented with numpy and the function implemented with builtin math return the same result.
from __future__ import annotations

import datetime

from typing import Callable, Tuple, List
import random
import timevec.builtin_math as tv
import timevec.numpy as tvn
import timevec.numpy_datetime64 as tv64
import numpy as np
import pytest


def assert_same(
    dt: datetime.datetime,
    func1: Callable[[datetime.datetime], Tuple[float, float]],
    func2: Callable[[datetime.datetime], np.ndarray],
    func3: Callable[[np.datetime64], np.ndarray],
    *,
    rel_tol: float = 1e-9,
    abs_tol: float = 0.0,
) -> None:
    """Assert that the functions return the same result."""
    dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
    result1 = func1(dt)
    result2 = func2(dt)
    result3 = func3(np.datetime64(dt))
    assert pytest.approx(result1[0], rel=rel_tol, abs=abs_tol) == result2[0] == result3[0]
    assert pytest.approx(result1[1], rel=rel_tol, abs=abs_tol) == result2[1] == result3[1]


def random_date() -> datetime.datetime:
    """Return a random datetime between 1990-01-01 and 2030-12-31."""
    year = random.randint(1990, 2030)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.datetime(year, month, day, hour, minute, second)


def random_dates(size: int = 2000) -> List[datetime.datetime]:
    """Return a list of random datetimes."""
    dates = []
    for _ in range(size):
        dates.append(random_date())
    return dates


def test_long_time_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, tv.long_time_vec, tvn.long_time_vec, tv64.long_time_vec)


def test_millennium_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, tv.millennium_vec, tvn.millennium_vec, tv64.millennium_vec)


def test_century_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, tv.century_vec, tvn.century_vec, tv64.century_vec)


def test_year_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, tv.year_vec, tvn.year_vec, tv64.year_vec)


def test_month_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, tv.month_vec, tvn.month_vec, tv64.month_vec)

    
def test_week_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, tv.week_vec, tvn.week_vec, tv64.week_vec)


def test_day_vec() -> None:
    test_dates = random_dates()
    for dt in test_dates:
        assert_same(dt, tv.day_vec, tvn.day_vec, tv64.day_vec)
