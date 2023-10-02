import unittest
from datetime import datetime
from muiscaenergy_common.src.timeseries.series_base import TimeSeries as TS


class TimeSeriesTest(unittest.TestCase):

    def test_get_ts(self):
        ts = TS(ts_from=datetime(2022, 4, 10),
                ts_to=datetime(2022, 4, 11),
                freq='15T')

        df = ts.get_ts()

        self.assertFalse(df.empty)
        self.assertTrue('datetime_local_from' in df.columns)
        self.assertTrue('datetime_local_to' in df.columns)

    def test_get_ts_tz(self):
        # tz = "America/New_York"; tz = "America/Los_Angeles"; tz = "America/Chicago";
        ts = TS(ts_from=datetime(2022, 4, 10),
                ts_to=datetime(2022, 4, 11),
                freq='H',
                tz="America/Los_Angeles")

        df = ts.get_ts_tz()

        self.assertFalse(df.empty)
        self.assertTrue('datetime_utc' in df.columns)
        self.assertTrue('datetime_local_from' in df.columns)
        self.assertTrue('datetime_local_to' in df.columns)

    def test_get_by_latlon(self):
        lat = 40.7128  # Nueva York
        lon = -74.0060
        ts = TS(ts_from=datetime(2022, 4, 10),
                ts_to=datetime(2022, 4, 11),
                freq='2D',
                lat=lat,
                lon=lon)
        df = ts.get_ts_latlon()

        self.assertFalse(df.empty)
        self.assertTrue('datetime_utc' in df.columns)
        self.assertTrue('datetime_local_from' in df.columns)
        self.assertTrue('datetime_local_to' in df.columns)

if __name__ == '__main__':
    unittest.main()
