import calendar
import datetime
from dataclasses import dataclass
from typing import Literal

TARGET = Literal[
    "long_time",
    "millennium",
    "century",
    "decade",
    "year",
    "month",
    "week",
    "day",
]


@dataclass
class DateTimeRange:
    begin: datetime.datetime
    end: datetime.datetime

    @property
    def total_time(self) -> datetime.timedelta:
        return self.end - self.begin

    @property
    def half_time(self) -> datetime.timedelta:
        return self.total_time / 2

    @property
    def quarter_time(self) -> datetime.timedelta:
        return self.total_time / 4

    def elapsed_time(self, current: datetime.datetime) -> datetime.timedelta:
        return current - self.begin

    def elapsed_time_by_ratio(
        self,
        ratio: float,
    ) -> datetime.timedelta:
        return ratio * self.total_time

    def current_time_by_ratio(
        self,
        ratio: float,
    ) -> datetime.datetime:
        return self.begin + self.elapsed_time_by_ratio(ratio)

    def time_elapsed_ratio(self, current: datetime.datetime) -> float:
        return (
            self.elapsed_time(current).total_seconds()
            / self.total_time.total_seconds()
        )

    @property
    def end_of_first_quarter(self) -> datetime.datetime:
        return self.begin + 1 * self.quarter_time

    @property
    def end_of_second_quarter(self) -> datetime.datetime:
        return self.begin + 2 * self.quarter_time

    @property
    def end_of_third_quarter(self) -> datetime.datetime:
        return self.begin + 3 * self.quarter_time


BEGIN_OF_DATETIME = datetime.datetime(1, 1, 1, 0, 0, 0)
END_OF_DATETIME = datetime.datetime(5001, 1, 1, 0, 0, 0)


def long_time_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    """Return a DateTimeRange that covers a long time period"""
    return DateTimeRange(
        begin=BEGIN_OF_DATETIME,
        end=END_OF_DATETIME,
    )


def millennium_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    """Return a DateTimeRange that covers a millennium"""
    begin_of_millennium = datetime.datetime.min.replace(
        year=(dt.year - 1) // 1000 * 1000 + 1,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_millennium = datetime.datetime.min.replace(
        year=(dt.year - 1) // 1000 * 1000 + 1001,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return DateTimeRange(begin_of_millennium, end_of_millennium)


def century_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    """Return a DateTimeRange that covers a century"""
    begin_of_century = datetime.datetime.min.replace(
        year=(dt.year - 1) // 100 * 100 + 1,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_century = datetime.datetime.min.replace(
        year=(dt.year - 1) // 100 * 100 + 101,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return DateTimeRange(begin_of_century, end_of_century)


def decade_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    """Return a DateTimeRange that covers a decade"""
    begin_of_decade = datetime.datetime.min.replace(
        year=dt.year // 10 * 10,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_decade = datetime.datetime.min.replace(
        year=dt.year // 10 * 10 + 10,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return DateTimeRange(begin_of_decade, end_of_decade)


def year_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    """Return a DateTimeRange that covers a year"""
    begin_of_year = datetime.datetime.min.replace(
        year=dt.year,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_year = datetime.datetime.min.replace(
        year=dt.year + 1,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    return DateTimeRange(begin_of_year, end_of_year)


def month_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    """Return a DateTimeRange that covers a month"""
    begin_of_month = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=1,
        hour=0,
        minute=0,
        second=0,
    )
    _, last_day = calendar.monthrange(dt.year, dt.month)
    end_of_month = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=last_day,
        hour=0,
        minute=0,
        second=0,
    ) + datetime.timedelta(days=1)
    return DateTimeRange(begin_of_month, end_of_month)


def week_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    """Return a DateTimeRange that covers a week"""
    begin_of_week = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    ) - datetime.timedelta(days=dt.weekday())
    end_of_week = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    ) + datetime.timedelta(days=7 - dt.weekday())
    return DateTimeRange(begin_of_week, end_of_week)


def day_range(
    dt: datetime.datetime,
) -> DateTimeRange:
    """Return a DateTimeRange that covers a day"""
    begin_of_day = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    )
    end_of_day = datetime.datetime.min.replace(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=0,
        minute=0,
        second=0,
    ) + datetime.timedelta(days=1)
    return DateTimeRange(begin_of_day, end_of_day)


__all__ = [
    "DateTimeRange",
    "long_time_range",
    "millennium_range",
    "century_range",
    "decade_range",
    "year_range",
    "month_range",
    "week_range",
    "day_range",
]
