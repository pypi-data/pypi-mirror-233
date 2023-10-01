from timezonefinder import TimezoneFinder
from datetime import timedelta, datetime
import pandas as pd


class TimeSeries:

    FREQ_MAP = {
        'T': timedelta(minutes=1),  # 30T
        'H': timedelta(hours=1),
        'D': timedelta(days=1)
    }

    def __init__(self,
                 ts_from: datetime = None,
                 ts_to: datetime = None,
                 freq: str = 'H',
                 lat: float = None,
                 lon: float = None,
                 tz: str = None):
        self.lat = lat
        self.lon = lon
        self.freq = freq
        self.ts_from = ts_from
        self.ts_to = ts_to
        self.tz = tz

    def get_by_freq(self):
        if self.freq is None:
            raise ValueError("The 'freq' parameter is required.")

        timeseries_from = pd.date_range(start=pd.to_datetime(self.ts_from),
                                        end=pd.to_datetime(self.ts_to),
                                        freq=self.freq)

        timeseries_to = timeseries_from + pd.Timedelta(self.parse_custom_freq(freq=self.freq))

        df = pd.DataFrame({'datetime_local_from': timeseries_from,
                           'datetime_local_to': timeseries_to
                           })

        return df

    def get_by_tz(self):
        if self.tz is None or self.freq is None:
            raise ValueError("The 'freq' and 'tz' parameters are required.")

        timeseries_from = pd.date_range(start=pd.to_datetime(self.ts_from),
                                        end=pd.to_datetime(self.ts_to),
                                        freq=self.freq,
                                        tz=self.tz)

        timeseries_gmt = timeseries_from.tz_convert('UTC')
        timeseries_to = timeseries_from + pd.Timedelta(self.parse_custom_freq(freq=self.freq))

        df = pd.DataFrame({'datetime_utc': timeseries_gmt,
                           'datetime_local_from': timeseries_from,
                           'datetime_local_to': timeseries_to
                           })

        return df

    def get_by_latlon(self):
        if self.lat is None or self.lon is None or self.freq is None:
            raise ValueError("The 'freq' and 'lat/lon' parameters are required.")

        timeseries_from = pd.date_range(start=pd.to_datetime(self.ts_from),
                                        end=pd.to_datetime(self.ts_to),
                                        freq=self.freq,
                                        tz=TimezoneFinder().timezone_at(lng=self.lon, lat=self.lat))

        timeseries_gmt = timeseries_from.tz_convert('UTC')
        timeseries_to = timeseries_from + pd.Timedelta(self.parse_custom_freq(freq=self.freq))

        df = pd.DataFrame({'datetime_utc': timeseries_gmt,
                           'datetime_local_from': timeseries_from,
                           'datetime_local_to': timeseries_to
                           })

        return df

    def parse_custom_freq(self, freq):
        num = ""
        unit = ""

        for char in freq:
            if char.isdigit():
                num += char
            else:
                unit += char

        if not num:
            num = "1"

        if unit == 'T':
            return pd.Timedelta(minutes=int(num))
        elif unit == 'H':
            return pd.Timedelta(hours=int(num))
        elif unit == 'D':
            return pd.Timedelta(days=int(num))
        else:
            raise ValueError("Invalid value for 'freq'.")
