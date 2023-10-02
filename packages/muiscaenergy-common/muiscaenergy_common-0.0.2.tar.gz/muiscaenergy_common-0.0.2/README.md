# Muisca Energy Commons
Common functions for muiscaenergy projects.

## Time Series

Example usage:

    from datetime import datetime
    from muiscaenergy_common.src.timeseries.series_base import TimeSeries

    # Create a TimeSeries instance
    ts = TimeSeries(ts_from=datetime(2023, 9, 30, 12, 0, 0),
                    ts_to=datetime(2023, 10, 1, 12, 0, 0),
                    freq='H',
                    lat=40.7128,
                    lon=-74.0060,
                    tz="America/New_York")

     # Generate a time series with ts_from, ts_to and freq
     df = ts.get_ts()

     # Generate a time series with a specific time zone
     df = ts.get_by_tz()

     # Generate a time series for a specific geographical location
     df = ts.get_by_latlon()


## Learning Material
# Espanol
https://www.youtube.com/watch?v=AczMuVzUrkE&ab_channel=SebastianBelmonte

# English
https://www.youtube.com/watch?v=5KEObONUkik&ab_channel=ArjanCodes