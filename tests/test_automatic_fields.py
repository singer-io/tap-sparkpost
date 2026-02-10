"""Test that with no fields selected for a stream automatic fields are still
replicated."""
from base import SparkpostBaseTest
from tap_tester.base_suite_tests.automatic_fields_test import MinimumSelectionTest


class SparkpostAutomaticFields(MinimumSelectionTest, SparkpostBaseTest):
    """Test that with no fields selected for a stream automatic fields are
    still replicated."""

    @staticmethod
    def name():
        return "tap_tester_sparkpost_automatic_fields_test"

    def streams_to_test(self):
        # Only metrics_time_series has ts in schema and data in test account
        return {"metrics_time_series"}

