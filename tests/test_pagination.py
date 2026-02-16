from tap_tester.base_suite_tests.pagination_test import PaginationTest
from base import SparkpostBaseTest

class SparkpostPaginationTest(PaginationTest, SparkpostBaseTest):
    """
    Ensure tap can replicate multiple pages of data for streams that use pagination.
    """

    @staticmethod
    def name():
        return "tap_tester_sparkpost_pagination_test"

    def streams_to_test(self):
        # Only metrics_time_series has enough records (1316) to test pagination
        return {"metrics_time_series"}
