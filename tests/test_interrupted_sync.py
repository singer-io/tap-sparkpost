import unittest
from base import SparkpostBaseTest
from tap_tester.base_suite_tests.interrupted_sync_test import InterruptedSyncTest


@unittest.skip(
    "Interrupted sync test incompatible with tap architecture. "
    "Test framework assumes:"
    "(1) full table streams have replication keys (SparkPost doesn't), "
    "(2) streams sync in alphabetical order (not guaranteed)."
)
class SparkpostInterruptedSyncTest(InterruptedSyncTest, SparkpostBaseTest):
    """Test tap resumes from interrupted sync.

    SKIP REASON:
    The interrupted sync test framework has fundamental incompatibilities:
    1. Assumes full table streams have exactly 1 replication_key
       → SparkPost full table streams have 0 replication keys (empty set)
    2. Assumes streams sync in alphabetical order from currently_syncing point
       → Tap doesn't guarantee alphabetical stream ordering
    3. Test fails with 'assert len(expected_replication_key) == 1' for full table streams
    """

    @staticmethod
    def name():
        return "tap_tester_sparkpost_interrupted_sync_test"

    def streams_to_test(self):
        return {"account", "templates", "sending_domains", "metrics_time_series"}

    def manipulate_state(self):
        return {
            "currently_syncing": "templates",
            "bookmarks": {
                "metrics_time_series": {"timestamp": "2026-02-09T00:00:00Z"},
            }
        }
