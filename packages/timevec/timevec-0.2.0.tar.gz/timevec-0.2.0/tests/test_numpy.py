import datetime

import numpy as np
import pytest

import timevec.numpy as tvn


def test_long_time_vec() -> None:
    dt = datetime.datetime(1, 1, 1, 0, 0, 0)
    vec = tvn.long_time_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(5001, 1, 1, 0, 0, 0)
    vec = tvn.long_time_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)


def test_millennium_vec() -> None:
    dt = datetime.datetime(2001, 1, 1, 0, 0, 0)
    vec = tvn.millennium_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(3001, 1, 1, 0, 0, 0)
    vec = tvn.millennium_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)


def test_century_vec() -> None:
    dt = datetime.datetime(2001, 1, 1, 0, 0, 0)
    vec = tvn.century_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2051, 1, 1, 0, 0, 0)
    vec = tvn.century_vec(dt)
    assert vec == pytest.approx(np.array([-1.0, 0.0]), abs=1e-6)


def test_year_vec() -> None:
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = tvn.year_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 7, 2, 12, 0, 0)
    vec = tvn.year_vec(dt)
    assert vec == pytest.approx(np.array([-1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 12, 31, 23, 59, 59)
    vec = tvn.year_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)


def test_month_vec() -> None:
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = tvn.month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 16, 12, 0, 0)
    vec = tvn.month_vec(dt)
    assert vec == pytest.approx(np.array([-1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 31, 23, 59, 59)
    vec = tvn.month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-5)


def test_week_vec() -> None:
    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)  # Monday
    vec = tvn.week_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 3, 0, 0, 0)  # Tuesday
    vec = tvn.week_vec(dt)
    assert vec == pytest.approx(np.array([0.623489, 0.781831]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 4, 0, 0, 0)  # Wednesday
    vec = tvn.week_vec(dt)
    assert vec == pytest.approx(np.array([-0.222521, 0.974928]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 5, 0, 0, 0)  # Thursday
    vec = tvn.week_vec(dt)
    assert vec == pytest.approx(np.array([-0.900969, 0.433884]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 6, 0, 0, 0)  # Friday
    vec = tvn.week_vec(dt)
    assert vec == pytest.approx(np.array([-0.900969, -0.433884]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 7, 0, 0, 0)  # Saturday
    vec = tvn.week_vec(dt)
    assert vec == pytest.approx(np.array([-0.222521, -0.974928]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 8, 0, 0, 0)  # Sunday
    vec = tvn.week_vec(dt)
    assert vec == pytest.approx(np.array([0.623489, -0.781831]), abs=1e-6)


def test_day_vec() -> None:
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = tvn.day_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 1, 12, 0, 0)
    vec = tvn.day_vec(dt)
    assert vec == pytest.approx(np.array([-1.0, 0.0]), abs=1e-6)


def test_edge_cases() -> None:
    # beginning of year
    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = tvn.year_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = tvn.month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 2, 0, 0, 0)  # Monday
    vec = tvn.week_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 1, 1, 0, 0, 0)
    vec = tvn.day_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    # end of year
    dt = datetime.datetime(2023, 12, 31, 23, 59, 59, 999999)
    vec = tvn.year_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-6)

    dt = datetime.datetime(2023, 12, 31, 23, 59, 59, 999999)
    vec = tvn.month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-5)

    dt = datetime.datetime(2023, 12, 31, 23, 59, 59, 999999)
    vec = tvn.day_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-4)

    # end of month
    dt = datetime.datetime(2023, 1, 31, 23, 59, 59, 999999)
    vec = tvn.month_vec(dt)
    assert vec == pytest.approx(np.array([1.0, 0.0]), abs=1e-5)
