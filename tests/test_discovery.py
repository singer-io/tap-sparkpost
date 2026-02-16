"""Test tap discovery mode and metadata."""
from base import SparkpostBaseTest
from tap_tester.base_suite_tests.discovery_test import DiscoveryTest
from tap_tester import menagerie


class SparkpostDiscoveryTest(DiscoveryTest, SparkpostBaseTest):
    """Test tap discovery mode and metadata conforms to standards."""
    orphan_streams = {
        "events",
        "webhooks",
        "templates",
        "sending_domains",
        "tracking_domains",
        "suppression_list",
        "recipient_lists",
        "account",
        "usage",
        "subaccounts",
        "ip_pools",
        "metrics_recipient_domain",
        "metrics_sending_ip",
        "metrics_ip_pool",
        "metrics_sending_domain",
        "metrics_subaccount",
        "metrics_campaign",
        "metrics_template",
        "metrics_subject_campaign",
        "metrics_watched_domain",
        "metrics_mailbox_provider",
        "metrics_mailbox_provider_region",
        "metrics_time_series",
        "metrics_bounce_reason",
        "metrics_bounce_reason_by_domain",
        "metrics_bounce_classification",
        "metrics_rejection_reason",
        "metrics_rejection_reason_by_domain",
        "metrics_delay_reason",
        "metrics_delay_reason_by_domain",
        "metrics_engagement_details",
        "metrics_deliveries_by_attempt",
    }

    @staticmethod
    def name():
        return "tap_tester_sparkpost_discovery_test"

    def streams_to_test(self):
        return self.expected_stream_names()

    def test_parent_stream(self):
        """
        Test that each stream's metadata correctly includes the expected parent tap stream ID.

        For each stream in `streams_to_test`, this test:
        - Retrieves the expected parent tap stream ID from test expectations.
        - Retrieves the actual metadata from the found catalog.
        - Verifies that the metadata contains the `PARENT_TAP_STREAM_ID` key (except for the orphans stream).
        - Confirms that the actual parent tap stream ID matches the expected value.
        """
        for stream in self.streams_to_test():
            with self.subTest(stream=stream):

                expected_parent_tap_stream_id = self.expected_parent_tap_stream(stream)

                catalogs = menagerie.get_catalogs(self.conn_id)
                catalog = [catalog for catalog in catalogs
                           if catalog["stream_name"] == stream][0]
                metadata = menagerie.get_annotated_schema(
                    self.conn_id, catalog['stream_id'])["metadata"]
                stream_properties = [item for item in metadata if item.get("breadcrumb") == []]
                actual_parent_tap_stream_id = \
                    stream_properties[0].get("metadata", {}).get(self.PARENT_TAP_STREAM_ID, None)


                self.assertIn("metadata", stream_properties[0])
                stream_metadata = stream_properties[0]["metadata"]


                if stream not in self.orphan_streams:
                    self.assertIn(self.PARENT_TAP_STREAM_ID, stream_metadata)
                    self.assertTrue(isinstance(actual_parent_tap_stream_id, str))


                with self.subTest(msg="validating parent tap stream id"):
                    self.assertEqual(expected_parent_tap_stream_id, actual_parent_tap_stream_id,
                                        logging=f"verify {expected_parent_tap_stream_id} "
                                                f"is saved in metadata as a parent-tap-stream-id")

