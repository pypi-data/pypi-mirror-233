# timevec

[![python versions](https://img.shields.io/pypi/pyversions/timevec)](https://pypi.org/project/timevec/)
[![package version](https://img.shields.io/pypi/v/timevec)](https://pypi.org/project/timevec/#history)
[![codecov](https://codecov.io/gh/kitsuyui/python-timevec/branch/main/graph/badge.svg?token=38BQRO1R00)](https://codecov.io/gh/kitsuyui/python-timevec)

Functions to create time vectors

# Description

Time has a periodic nature due to the rotation of the earth and the position of the sun.
This affects human behavior in various ways.

- Seasonality ... periodicity in a year (seasonal distinction)
- Daily periodicity ... periodicity in a day (distinction between day and night)
- Day of the week ... periodicity in a week (distinction between weekdays and holidays)

When dealing with these, it is desirable to vectorize with periodicity in mind.
That is, at 23:59 on a given day, it is desirable that the value is close to 00:00 on the next day.
To achieve this, the time is represented as a combination of cos and sin.
This is called a time vector.

# Installation

```sh
pip install timevec
```

# Usage

```python
import timevec.numpy as tv
import datetime
dt = datetime.datetime(2020, 1, 1, 0, 0, 0)
vec = tv.year_vec(dt)
# array([1., 0.])
```

# Modules

- `timevec.numpy` provides functions that return numpy.ndarray.
- `timevec.numpy_datetime64` provides functions that return numpy.datetime64.
- `timevec.builtin_math` provides functions that return tuple of float.

# Functions

Almost same functions are provided in `timevec.numpy`, `timevec.numpy_datetime64`, and `timevec.builtin_math`.
The difference is the return type.

## year_vec

```python
year_vec(dt: datetime.datetime)
```

Create a time vector for a year.
This is a vector that has periodicity like seasonality.
(Summer, Autumn, Winter, Spring)
![year_vec](https://user-images.githubusercontent.com/2596972/213921526-f59c44d1-22c1-4649-88ca-5f50b8d85765.svg)

## month_vec

```python
month_vec(dt: datetime.datetime)
```

Create a time vector for a month.
This is a vector that has periodicity in a month.
You can express periodicity such as the beginning of the month, the end of the month, and the salary day.
![month_vec](https://user-images.githubusercontent.com/2596972/213921552-6369b8f0-6eff-42fd-8f9f-42a9ad62f2b8.svg)


## week_vec

```python
week_vec(dt: datetime.datetime)
```

Create a time vector for a week.
This is a vector that has periodicity in a week.
You can express periodicity such as weekdays and holidays.
![week_vec](https://user-images.githubusercontent.com/2596972/213921560-eb7b4e6d-bfc7-487a-926b-2810365ba8d8.svg)


## day_vec

```python
day_vec(dt: datetime.datetime)
```

Create a time vector for a day.
This is a vector that has periodicity in a day.
You can express periodicity such as morning, noon, and night.
![day_vec](https://user-images.githubusercontent.com/2596972/213921566-dd69416e-2816-4c3d-9808-b3f87a51e543.svg)


## Others

- `long_time_vec` ... 1 to 5001 years period
- `millennium_vec` ... one millennium (1000 years) period
- `century_vec` ... one century (100 years) period
- `decade_vec` ... one decade (10 years) period

# License

BSD 3-Clause License
