# pip install .
from datetime import datetime
from muiscaenergy_common.src.timeseries.series_base import TimeSeries

ts = TimeSeries(ts_from=datetime(2023, 9, 30, 12, 0, 0),
                ts_to=datetime(2023, 10, 1, 12, 0, 0),
                freq='H',
                lat=40.7128,
                lon=-74.0060,
                tz="America/New_York")

# Generate a time series with ts_from, ts_to and freq
df1 = ts.get_ts()
print(df1)

# Generate a time series with a specific time zone
df2 = ts.get_ts_tz()
print(df2)

# Generate a time series for a specific geographical location
df3 = ts.get_ts_latlon()
print(df3)
