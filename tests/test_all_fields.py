from base import SparkpostBaseTest
from tap_tester.base_suite_tests.all_fields_test import AllFieldsTest


class SparkpostAllFields(AllFieldsTest, SparkpostBaseTest):
    """Ensure running the tap with all streams and fields selected results in
    the replication of all fields."""
    
    MISSING_FIELDS = {
        "account": {"pending_cancellation", "pending_subscription", "usage", "support"},
        "usage": {"messaging", "recipient_validation"},
        "templates": {"content", "last_use", "options"},
        "subaccounts": {"ip_pool"},
        "sending_domains": {"dkim", "delegated", "subaccount_id", "tracking_domain"},
        "ip_pools": {"fbl_signing_domain", "auto_warmup_overflow_pool", "signing_domain"},
        "metrics_time_series": {
            "total_delivery_time_first",
            "count_unique_confirmed_opened",
            "count_unique_clicked",
            "count_generation_failed",
            "count_outofband_bounce",
            "count_delivered_first",
            "count_inband_bounce",
            "count_soft_bounce",
            "count_delayed",
            "count_injected",
            "count_admin_bounce",
            "total_msg_volume",
            "count_hard_bounce",
            "count_clicked",
            "total_delivery_time_subsequent",
            "count_generation_rejection",
            "count_undetermined_bounce",
            "count_rendered",
            "count_policy_rejection",
            "count_delayed_first",
            "count_block_bounce",
            "count_unique_rendered",
            "count_delivered_subsequent",
            "count_bounce",
            "count_spam_complaint",
            "count_rejected",
        },
    }

    @staticmethod
    def name():
        return "tap_tester_sparkpost_all_fields_test"

    def streams_to_test(self):
        # Streams with data in test account and compatible API plan
        return {
            "templates",
            "sending_domains",
            "account",
            "usage",
            "subaccounts",
            "ip_pools",
            "metrics_time_series",
        }

