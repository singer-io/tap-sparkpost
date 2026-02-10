import unittest
from base import SparkpostBaseTest
from tap_tester.base_suite_tests.start_date_test import StartDateTest


@unittest.skip("SparkPost Metrics API returns historical data spanning 2025-2026 regardless of "
               "start_date parameter. The API does not filter by the 'from' parameter for metrics "
               "time series data in a way that allows start_date validation.")
class SparkpostStartDateTest(StartDateTest, SparkpostBaseTest):
    """Test start date handling for tap-sparkpost.

    NOTE: This test is skipped because the SparkPost Metrics API returns
    all historical data in the account (dating back to 2025) regardless
    of the start_date/from parameter, making it impossible to validate
    start_date filtering behavior.
    """

    @staticmethod
    def name():
        return "tap_tester_sparkpost_start_date_test"

    def streams_to_test(self):
        return {"metrics_time_series"}

    @property
    def start_date_1(self):
        return "2026-02-06T00:00:00Z"

    @property
    def start_date_2(self):
        return "2026-02-06T13:00:00Z"
