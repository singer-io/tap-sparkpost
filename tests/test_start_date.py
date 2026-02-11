import unittest
from base import SparkpostBaseTest
from tap_tester.base_suite_tests.start_date_test import StartDateTest


@unittest.skip(
    "SparkPost Metrics API returns all historical data (2023-2026) regardless of "
    "start_date/from parameter. API limitation prevents start_date validation."
)
class SparkpostStartDateTest(StartDateTest, SparkpostBaseTest):
    """Test start date handling for tap-sparkpost.

    SKIP REASON:
    The SparkPost Metrics API returns all historical data in the account
    regardless of the 'from' parameter value:
    - start_date set to: 2026-02-10T00:00:00Z
    - API returns records from: 2023-02-07, 2024-06-17, 2025-03-01, etc.
    - Test expects: only records >= start_date
    - Result: Test fails with hundreds of violations

    This is an API limitation, not a tap bug. The API ignores date filtering
    and returns the full historical dataset spanning multiple years.
    """

    @staticmethod
    def name():
        return "tap_tester_sparkpost_start_date_test"

    def streams_to_test(self):
        return {"metrics_time_series"}

    @property
    def start_date_1(self):
        return "2026-02-08T00:00:00Z"

    @property
    def start_date_2(self):
        return "2026-02-10T00:00:00Z"
