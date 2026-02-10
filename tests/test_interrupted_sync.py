import unittest
from base import SparkpostBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


@unittest.skip("Only metrics_time_series has data in test account. "
               "Interrupted sync test requires multiple streams with data.")
class SparkpostInterruptedSyncTest(InterruptedSyncTest, SparkpostBaseTest):
    """Test tap resumes from interrupted sync.

    NOTE: Only metrics_time_series has sufficient data in the test account.
    The interrupted sync test requires multiple streams with data to validate
    stream ordering after an interruption, so this test class is skipped.
    """

    @staticmethod
    def name():
        return "tap_tester_sparkpost_interrupted_sync_test"

    def streams_to_test(self):
        return {"metrics_time_series"}

    def manipulate_state(self):
        return {
            "currently_syncing": "metrics_time_series",
            "bookmarks": {
                "metrics_time_series": {"ts": "2022-07-01T00:00:00Z"},
            }
        }
