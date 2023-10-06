import datetime

from timevec.util import (
    day_range,
    month_range,
    week_range,
    century_range,
    millennium_range,
    long_time_range,
    year_range,
    DateTimeRange,
)


def assert_date_time_range(range: DateTimeRange) -> None:
    """Assert that a DateTimeRange is valid"""
    assert range.begin <= range.end
    assert range.total_time == 2 * range.half_time == 4 * range.quarter_time
    assert (
        range.begin
        < range.end_of_first_quarter
        < range.end_of_second_quarter
        < range.end_of_third_quarter
        < range.end
    )


def test_date_time_range() -> None:
    """Test DateTimeRange"""
    range = DateTimeRange(
        datetime.datetime(2000, 1, 1), datetime.datetime(2000, 1, 2)
    )
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(2000, 1, 1)
    assert range.end == datetime.datetime(2000, 1, 2)
    assert range.total_time == datetime.timedelta(days=1)


def test_long_time_range() -> None:
    """Test long_time_range()"""
    range = long_time_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(1, 1, 1)
    assert range.end == datetime.datetime(5001, 1, 1)
    assert range.total_time == datetime.timedelta(
        days=1826212
    )  # 5000 years contains 1212 leap years


def test_millennium_range() -> None:
    """Test millennium_range()"""
    range = millennium_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(1001, 1, 1)
    assert range.end == datetime.datetime(2001, 1, 1)
    assert range.total_time == datetime.timedelta(days=365243)


def test_century_range() -> None:
    """Test century_range()"""
    range = century_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(1901, 1, 1)
    assert range.end == datetime.datetime(2001, 1, 1)
    assert range.total_time == datetime.timedelta(days=36525)


def test_year_range() -> None:
    """Test year_range()"""
    range = year_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(2000, 1, 1)
    assert range.end == datetime.datetime(2001, 1, 1)
    assert range.total_time == datetime.timedelta(days=366)


def test_month_range() -> None:
    """Test month_range()"""
    range = month_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(2000, 1, 1)
    assert range.end == datetime.datetime(2000, 2, 1)
    assert range.total_time == datetime.timedelta(days=31)


def test_week_range() -> None:
    """Test week_range()"""
    range = week_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(1999, 12, 27)
    assert range.end == datetime.datetime(2000, 1, 3)
    assert range.total_time == datetime.timedelta(days=7)


def test_day_range() -> None:
    """Test day_range()"""
    range = day_range(datetime.datetime(2000, 1, 1))
    assert_date_time_range(range)
    assert range.begin == datetime.datetime(2000, 1, 1)
    assert range.end == datetime.datetime(2000, 1, 2)
    assert range.total_time == datetime.timedelta(days=1)
