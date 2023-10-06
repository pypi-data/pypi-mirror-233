import timevec.numpy as tvn
import timevec.numpy_datetime64 as tv64
import timevec.builtin_math as tv
import numpy as np
import datetime

import pytest


def test_many_dates() -> None:
    # start 1-01-01
    dt = datetime.datetime(11, 1, 1, 0, 0, 0)
    full = ['long_time', 'millennium', 'century', 'decade', 'year', 'month', 'week', 'day']
    minimal = ['long_time', 'century', 'year', 'day']


    # try all the functions does not raise an exception
    for i in range(50000):
        dt += datetime.timedelta(days=17, hours=13, minutes=11, seconds=7)

        vecs2 = tv.datetime_to_vecs(dt, full)
        dt2 = tv.datetime_from_vecs(vecs2)
        assert dt == dt2

        vecs3 = tv.datetime_to_vecs(dt, minimal)
        dt3 = tv.datetime_from_vecs(vecs3)
        assert dt == dt3

        vecs4 = tvn.datetime_to_vecs(dt, full)
        dt4 = tvn.datetime_from_vecs(vecs4)
        assert dt == dt4

        vecs5 = tvn.datetime_to_vecs(dt, minimal)
        dt5 = tvn.datetime_from_vecs(vecs5)
        assert dt == dt5

        vecs6 = tv64.datetime64_to_vecs(np.datetime64(dt), full)
        tv64.datetime64_from_vecs(vecs6)

        vecs7 = tv64.datetime64_to_vecs(np.datetime64(dt), minimal)
        tv64.datetime64_from_vecs(vecs7)

    # tested up to 2100-01-01
    assert dt >= datetime.datetime(2400, 1, 1, 0, 0, 0)
