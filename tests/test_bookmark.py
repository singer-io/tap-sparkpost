from base import SparkpostBaseTest
from tap_tester.base_suite_tests.bookmark_test import BookmarkTest


class SparkpostBookMarkTest(BookmarkTest, SparkpostBaseTest):
    """Test tap sets a bookmark and respects it for the next sync of a
    stream."""
    # Tap writes bookmarks in full ISO-8601 format: YYYY-MM-DDTHH:MM:SSZ
    bookmark_format = "%Y-%m-%dT%H:%M:%SZ"

    # SparkPost metrics API returns data in time buckets, so we need a lookback
    # to account for records that may appear in earlier time buckets
    timedelta_by_stream = {
        "metrics_time_series": {"hours": 1}  # 1 hour lookback for time-series metrics
    }

    initial_bookmarks = {
        "bookmarks": {
            "metrics_time_series": { "timestamp" : "2020-01-01T00:00:00Z"},
        }
    }

    @staticmethod
    def name():
        return "tap_tester_sparkpost_bookmark_test"

    def streams_to_test(self):
        # Only metrics_time_series has sufficient incremental data in test account
        return {"metrics_time_series"}
