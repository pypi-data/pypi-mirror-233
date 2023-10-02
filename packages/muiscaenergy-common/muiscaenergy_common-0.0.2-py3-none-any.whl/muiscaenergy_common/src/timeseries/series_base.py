from timezonefinder import TimezoneFinder
from datetime import timedelta, datetime
import pandas as pd


class TimeSeries:
    """
    TimeSeries class for generating time series data based on different parameters.
    Range (ts_from, ts_to) and frequency (freq) of series are required parameters.
    Location by latitude and longitude (lat, lon) or time zone (tz) are optional parameters.

    Attributes:
        FREQ_MAP (dict): A mapping of frequency units to timedelta values.
            Supported units: 'T' (minutes), 'H' (hours), 'D' (days).
        ts_from (datetime, optional): The start date and time for the time series.
        ts_to (datetime, optional): The end date and time for the time series.
        freq (str, optional): The frequency unit for the time series. Default is 'H' (hours).
        lat (float, optional): Latitude for geographical time zone information.
        lon (float, optional): Longitude for geographical time zone information.
        tz (str, optional): Time zone identifier.

    Methods:
        get_ts(self): Generates a time series based on the Range (ts_from, ts_to) and frequency (freq) .
        get_ts_tz(self): Generates a time series with specified time zone information.
        get_ts_latlon(self): Generates a time series for a specific geographical location.
        parse_custom_freq(self, freq): Parses custom frequency strings to timedelta values.

    Example usage:
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
    """

    FREQ_MAP = {
        'T': timedelta(minutes=1),
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

    def get_ts(self):
        """
        Generate a time series based on the specified frequency.

        Returns:
            pd.DataFrame: A DataFrame containing the generated time series.
        """

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

    def get_ts_tz(self):
        """
        Generate a time series with specified time zone information.

        Returns:
            pd.DataFrame: A DataFrame containing the generated time series with time zone information.
        """

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

    def get_ts_latlon(self):
        """
        Generate a time series for a specific geographical location.

        Returns:
            pd.DataFrame: A DataFrame containing the generated time series for the specified location.
        """

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



    # def get_by_freq(self):
    #     """
    #     Generate a time series based on the specified frequency.
    #
    #     Returns:
    #         pd.DataFrame: A DataFrame containing the generated time series.
    #     """
    #
    #     if self.freq is None:
    #         raise ValueError("The 'freq' parameter is required.")
    #
    #     timeseries_from = pd.date_range(start=pd.to_datetime(self.ts_from),
    #                                     end=pd.to_datetime(self.ts_to),
    #                                     freq=self.freq)
    #
    #     timeseries_to = timeseries_from + pd.Timedelta(self.parse_custom_freq(freq=self.freq))
    #
    #     df = pd.DataFrame({'datetime_local_from': timeseries_from,
    #                        'datetime_local_to': timeseries_to
    #                        })
    #
    #     return df
    #
    # def get_by_tz(self):
    #     """
    #     Generate a time series with specified time zone information.
    #
    #     Returns:
    #         pd.DataFrame: A DataFrame containing the generated time series with time zone information.
    #     """
    #
    #     if self.tz is None or self.freq is None:
    #         raise ValueError("The 'freq' and 'tz' parameters are required.")
    #
    #     timeseries_from = pd.date_range(start=pd.to_datetime(self.ts_from),
    #                                     end=pd.to_datetime(self.ts_to),
    #                                     freq=self.freq,
    #                                     tz=self.tz)
    #
    #     timeseries_gmt = timeseries_from.tz_convert('UTC')
    #     timeseries_to = timeseries_from + pd.Timedelta(self.parse_custom_freq(freq=self.freq))
    #
    #     df = pd.DataFrame({'datetime_utc': timeseries_gmt,
    #                        'datetime_local_from': timeseries_from,
    #                        'datetime_local_to': timeseries_to
    #                        })
    #
    #     return df
    #
    # def get_by_latlon(self):
    #     """
    #     Generate a time series for a specific geographical location.
    #
    #     Returns:
    #         pd.DataFrame: A DataFrame containing the generated time series for the specified location.
    #     """
    #
    #     if self.lat is None or self.lon is None or self.freq is None:
    #         raise ValueError("The 'freq' and 'lat/lon' parameters are required.")
    #
    #     timeseries_from = pd.date_range(start=pd.to_datetime(self.ts_from),
    #                                     end=pd.to_datetime(self.ts_to),
    #                                     freq=self.freq,
    #                                     tz=TimezoneFinder().timezone_at(lng=self.lon, lat=self.lat))
    #
    #     timeseries_gmt = timeseries_from.tz_convert('UTC')
    #     timeseries_to = timeseries_from + pd.Timedelta(self.parse_custom_freq(freq=self.freq))
    #
    #     df = pd.DataFrame({'datetime_utc': timeseries_gmt,
    #                        'datetime_local_from': timeseries_from,
    #                        'datetime_local_to': timeseries_to
    #                        })
    #
    #     return df
    #
    # def parse_custom_freq(self, freq):
    #     num = ""
    #     unit = ""
    #
    #     for char in freq:
    #         if char.isdigit():
    #             num += char
    #         else:
    #             unit += char
    #
    #     if not num:
    #         num = "1"
    #
    #     if unit == 'T':
    #         return pd.Timedelta(minutes=int(num))
    #     elif unit == 'H':
    #         return pd.Timedelta(hours=int(num))
    #     elif unit == 'D':
    #         return pd.Timedelta(days=int(num))
    #     else:
    #         raise ValueError("Invalid value for 'freq'.")

# class TimeSeries:
#
#     FREQ_MAP = {
#         'T': timedelta(minutes=1),  # 30T
#         'H': timedelta(hours=1),
#         'D': timedelta(days=1)
#     }
#
#     def __init__(self,
#                  ts_from: datetime = None,
#                  ts_to: datetime = None,
#                  freq: str = 'H',
#                  lat: float = None,
#                  lon: float = None,
#                  tz: str = None):
#         self.lat = lat
#         self.lon = lon
#         self.freq = freq
#         self.ts_from = ts_from
#         self.ts_to = ts_to
#         self.tz = tz
#
#     def get_by_freq(self):
#         if self.freq is None:
#             raise ValueError("The 'freq' parameter is required.")
#
#         timeseries_from = pd.date_range(start=pd.to_datetime(self.ts_from),
#                                         end=pd.to_datetime(self.ts_to),
#                                         freq=self.freq)
#
#         timeseries_to = timeseries_from + pd.Timedelta(self.parse_custom_freq(freq=self.freq))
#
#         df = pd.DataFrame({'datetime_local_from': timeseries_from,
#                            'datetime_local_to': timeseries_to
#                            })
#
#         return df
#
#     def get_by_tz(self):
#         if self.tz is None or self.freq is None:
#             raise ValueError("The 'freq' and 'tz' parameters are required.")
#
#         timeseries_from = pd.date_range(start=pd.to_datetime(self.ts_from),
#                                         end=pd.to_datetime(self.ts_to),
#                                         freq=self.freq,
#                                         tz=self.tz)
#
#         timeseries_gmt = timeseries_from.tz_convert('UTC')
#         timeseries_to = timeseries_from + pd.Timedelta(self.parse_custom_freq(freq=self.freq))
#
#         df = pd.DataFrame({'datetime_utc': timeseries_gmt,
#                            'datetime_local_from': timeseries_from,
#                            'datetime_local_to': timeseries_to
#                            })
#
#         return df
#
#     def get_by_latlon(self):
#         if self.lat is None or self.lon is None or self.freq is None:
#             raise ValueError("The 'freq' and 'lat/lon' parameters are required.")
#
#         timeseries_from = pd.date_range(start=pd.to_datetime(self.ts_from),
#                                         end=pd.to_datetime(self.ts_to),
#                                         freq=self.freq,
#                                         tz=TimezoneFinder().timezone_at(lng=self.lon, lat=self.lat))
#
#         timeseries_gmt = timeseries_from.tz_convert('UTC')
#         timeseries_to = timeseries_from + pd.Timedelta(self.parse_custom_freq(freq=self.freq))
#
#         df = pd.DataFrame({'datetime_utc': timeseries_gmt,
#                            'datetime_local_from': timeseries_from,
#                            'datetime_local_to': timeseries_to
#                            })
#
#         return df
#
#     def parse_custom_freq(self, freq):
#         num = ""
#         unit = ""
#
#         for char in freq:
#             if char.isdigit():
#                 num += char
#             else:
#                 unit += char
#
#         if not num:
#             num = "1"
#
#         if unit == 'T':
#             return pd.Timedelta(minutes=int(num))
#         elif unit == 'H':
#             return pd.Timedelta(hours=int(num))
#         elif unit == 'D':
#             return pd.Timedelta(days=int(num))
#         else:
#             raise ValueError("Invalid value for 'freq'.")
