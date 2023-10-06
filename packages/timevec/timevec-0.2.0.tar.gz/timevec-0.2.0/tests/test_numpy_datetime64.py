import datetime

import numpy as np
import pytest

import timevec.numpy_datetime64 as tv64
import timevec.numpy as tv


def test_long_time_vec() -> None:
    dt = datetime.datetime.now()
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.long_time_vec(dt64), tv.long_time_vec(dt))


def test_millennium_vec() -> None:
    dt = datetime.datetime.now()
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.millennium_vec(dt64), tv.millennium_vec(dt))


def test_century_vec() -> None:
    dt = datetime.datetime.now()
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.century_vec(dt64), tv.century_vec(dt))


def test_year_vec() -> None:
    dt = datetime.datetime.now()
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.year_vec(dt64), tv.year_vec(dt))


def test_month_vec() -> None:
    dt = datetime.datetime.now()
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.month_vec(dt64), tv.month_vec(dt))


def test_week_vec() -> None:
    dt = datetime.datetime.now()
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.week_vec(dt64), tv.week_vec(dt))


def test_day_vec() -> None:
    dt = datetime.datetime.now()
    dt64 = np.datetime64(dt)
    assert np.allclose(tv64.day_vec(dt64), tv.day_vec(dt))


def test_multiple_datetime64() -> None:
    dt = datetime.datetime.now()
    dt64 = np.datetime64(dt)
    vec = np.array([dt64, dt64, dt64], dtype=np.datetime64)
    assert vec.shape == (3,)
    vec2 = np.frompyfunc(tv64.day_vec, 1, 1)(vec)
    assert np.stack(vec2, axis=0).shape == (3, 2)
    vec3 = np.array([[dt64, dt64, dt64],
                     [dt64, dt64, dt64]], dtype=np.datetime64)
    assert vec3.shape == (2, 3)
