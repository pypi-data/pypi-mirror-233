"""Time vector representation

Time has a periodic nature due to the rotation of the earth and the position of the sun.
This affects human behavior in various ways.

Seasonality ... periodicity in a year (seasonal distinction)
Daily periodicity ... periodicity in a day (distinction between day and night)
Day of the week ... periodicity in a week (distinction between weekdays and holidays)

When dealing with these, it is desirable to vectorize with periodicity in mind.
That is, at 23:59 on a given day, it is desirable that the value is close to 00:00 on the next day.
To achieve this, the time is represented as a combination of cos and sin."""
