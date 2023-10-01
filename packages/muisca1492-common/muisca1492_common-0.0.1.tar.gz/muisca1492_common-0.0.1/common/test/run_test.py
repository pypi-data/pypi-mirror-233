import unittest
from common.test.timeseries.series_base import TimeSeriesTest


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TimeSeriesTest)

    runner = unittest.TextTestRunner()
    result = runner.run(suite)