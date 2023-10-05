# pip install .
from datetime import datetime
from muiscaenergy_common.src.timeseries.base import get_timeseries


ts_from = datetime(2023, 9, 30, 12, 0, 0)
ts_to = datetime(2023, 10, 1, 11, 0, 0)
freq = 'H'
lat = 52.5200
lon = 13.4050
tz = 'America/Los_Angeles'

# Get a TimeSeriesMessage object without notion of location
ts1 = get_timeseries(ts_from=ts_from,
                     ts_to=ts_to,
                     freq=freq)
print(ts1.df)

# Get a TimeSeriesMessage object with notion of location via lat and lon
ts2 = get_timeseries(ts_from=ts_from,
                     ts_to=ts_to,
                     freq=freq,
                     lat=lat,
                     lon=lon)
print(ts2.df)

# Get a TimeSeriesMessage object with notion of location via tz (timezone)
ts3 = get_timeseries(ts_from=ts_from,
                     ts_to=ts_to,
                     freq=freq,
                     tz=tz)
print(ts3.df)

