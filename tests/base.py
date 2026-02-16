import os

from tap_tester import connections, menagerie
from tap_tester.base_suite_tests.base_case import BaseCase


class SparkpostBaseTest(BaseCase):
    """Setup expectations for test sub classes.

    Metadata describing streams. A bunch of shared methods that are used
    in tap-tester tests. Shared tap-specific methods (as needed).
    """
    start_date = "2026-02-06T00:00:00Z"
    PARENT_TAP_STREAM_ID = "parent-tap-stream-id"

    @staticmethod
    def tap_name():
        """The name of the tap."""
        return "tap-sparkpost"

    @staticmethod
    def get_type():
        """The name of the tap."""
        return "platform.sparkpost"

    @classmethod
    def expected_metadata(cls):
        """The expected streams and metadata about the streams."""
        return {
            # Non-metrics streams
            "events": {
                cls.PRIMARY_KEYS: {"event_id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "webhooks": {
                cls.PRIMARY_KEYS: {"id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"last_successful", "last_failure"},
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "templates": {
                cls.PRIMARY_KEYS: {"id"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "sending_domains": {
                cls.PRIMARY_KEYS: {"domain"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "tracking_domains": {
                cls.PRIMARY_KEYS: {"domain"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "suppression_list": {
                cls.PRIMARY_KEYS: {"recipient"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "recipient_lists": {
                cls.PRIMARY_KEYS: {"id"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "account": {
                cls.PRIMARY_KEYS: {"customer_id"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "usage": {
                cls.PRIMARY_KEYS: {"timestamp"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "subaccounts": {
                cls.PRIMARY_KEYS: {"id"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            "ip_pools": {
                cls.PRIMARY_KEYS: {"id"},
                cls.REPLICATION_METHOD: cls.FULL_TABLE,
                cls.REPLICATION_KEYS: set(),
                cls.OBEYS_START_DATE: False,
                cls.API_LIMIT: 100
            },
            # Metrics streams - all INCREMENTAL with "timestamp" replication key
            # Note: API returns 'ts' but modify_object() renames it to 'timestamp'
            # All metrics streams include timestamp as part of composite primary key
            "metrics_recipient_domain": {
                cls.PRIMARY_KEYS: {"timestamp", "domain"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_sending_ip": {
                cls.PRIMARY_KEYS: {"timestamp", "sending_ip"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_ip_pool": {
                cls.PRIMARY_KEYS: {"timestamp", "ip_pool"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_sending_domain": {
                cls.PRIMARY_KEYS: {"timestamp", "sending_domain"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_subaccount": {
                cls.PRIMARY_KEYS: {"timestamp", "subaccount_id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_campaign": {
                cls.PRIMARY_KEYS: {"timestamp", "campaign_id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_template": {
                cls.PRIMARY_KEYS: {"timestamp", "template_id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_subject_campaign": {
                cls.PRIMARY_KEYS: {"timestamp", "subject_campaign"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_watched_domain": {
                cls.PRIMARY_KEYS: {"timestamp", "watched_domain"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_mailbox_provider": {
                cls.PRIMARY_KEYS: {"timestamp", "mailbox_provider"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_mailbox_provider_region": {
                cls.PRIMARY_KEYS: {"timestamp", "mailbox_provider_region"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_time_series": {
                cls.PRIMARY_KEYS: {"timestamp"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_bounce_reason": {
                cls.PRIMARY_KEYS: {"timestamp", "reason", "classification_id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_bounce_reason_by_domain": {
                cls.PRIMARY_KEYS: {"timestamp", "reason", "domain", "classification_id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_bounce_classification": {
                cls.PRIMARY_KEYS: {"timestamp", "classification_id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_rejection_reason": {
                cls.PRIMARY_KEYS: {"timestamp", "reason", "rejection_category_id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_rejection_reason_by_domain": {
                cls.PRIMARY_KEYS: {"timestamp", "reason", "domain", "rejection_category_id"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_delay_reason": {
                cls.PRIMARY_KEYS: {"timestamp", "reason"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_delay_reason_by_domain": {
                cls.PRIMARY_KEYS: {"timestamp", "reason", "domain"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_engagement_details": {
                cls.PRIMARY_KEYS: {"timestamp", "link_name"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            },
            "metrics_deliveries_by_attempt": {
                cls.PRIMARY_KEYS: {"timestamp", "attempt"},
                cls.REPLICATION_METHOD: cls.INCREMENTAL,
                cls.REPLICATION_KEYS: {"timestamp"},
                cls.OBEYS_START_DATE: True,
                cls.API_LIMIT: 100
            }
        }

    @staticmethod
    def get_credentials():
        """Authentication information for the test account."""
        return {}

    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return_value = {
            "api_key": os.getenv('TAP_SPARKPOST_API_KEY'),
            "start_date": "2022-07-01T00:00:00Z",
            "base_url": os.getenv('TAP_SPARKPOST_BASE_URL', 'https://api.sparkpost.com/api/v1')
        }
        if original:
            return return_value

        return_value["start_date"] = self.start_date
        return return_value

    def expected_parent_tap_stream(self, stream=None):
        """return a dictionary with key of table name and value of parent stream"""
        parent_stream = {
            table: properties.get(self.PARENT_TAP_STREAM_ID, None)
            for table, properties in self.expected_metadata().items()}
        if not stream:
            return parent_stream
        return parent_stream[stream]

    def expected_automatic_fields(self, stream=None):
        """
        Override to match tap's actual behavior for automatic field selection.
        
        CHANGE REASON:
        The discovery test was failing because it expected only replication keys to be
        marked as automatic, but the tap actually marks BOTH primary keys AND replication
        keys as automatic fields. This is the standard Singer behavior.
        
        SINGER SPECIFICATION:
        Automatic fields are fields that the tap will always sync, regardless of user
        selection. These typically include:
        1. Primary keys (key_properties) - required for record identification
        2. Replication keys - required for incremental sync state management
        
        SPARKPOST-SPECIFIC BEHAVIOR:
        The tap marks both primary keys AND replication keys as automatic. However,
        for most metrics streams, the replication key 'ts' (timestamp) is NOT included
        in the schema properties definition, even though it's defined as a replication
        key in the stream class. This means:
        
        - If a field is not in the schema, it cannot be marked as automatic in metadata
        - The Singer transformer won't process fields that aren't in the schema
        
        EXAMPLES:
        1. Non-metrics stream (e.g., 'events'):
           - Primary keys: {"event_id"}
           - Replication keys: {"timestamp"}
           - Automatic fields: {"event_id", "timestamp"} ← Both are in schema
        
        2. Metrics stream without ts (e.g., 'metrics_campaign'):
           - Primary keys: {"campaign_id"}
           - Replication keys: {"ts"}
           - Automatic fields: {"campaign_id"} ← Only primary key, ts not in schema
        
        3. Metrics stream with ts (e.g., 'metrics_time_series'):
           - Primary keys: {"ts"}
           - Replication keys: {"ts"}
           - Automatic fields: {"ts"} ← ts is BOTH primary and replication key, in schema
        
        IMPLEMENTATION:
        - Non-metrics streams: return primary keys + replication keys
        - Most metrics streams: return primary keys only (ts not in schema)
        - metrics_time_series: return {"ts"} (ts is both primary and replication key)
        """
        # All metrics streams now have timestamp in schema (renamed from ts)
        # No special handling needed - all streams include replication keys as automatic
        metrics_streams_without_timestamp_in_schema = set()  # Empty set - all have timestamp now
        
        automatic_fields = {}
        for table, properties in self.expected_metadata().items():
            # Start with primary keys as automatic fields
            auto_fields = properties.get(self.PRIMARY_KEYS, set()).copy()
            
            if table in metrics_streams_without_timestamp_in_schema:
                # These metrics streams have timestamp as replication key but it's not in schema
                # Only primary keys are automatic
                pass
            else:
                # All streams: add replication keys as automatic
                auto_fields.update(properties.get(self.REPLICATION_KEYS, set()))
            
            automatic_fields[table] = auto_fields
        
        if not stream:
            return automatic_fields
        return automatic_fields[stream]

    def perform_and_verify_table_and_field_selection(self, conn_id, test_catalogs):
        """
        Override base method to explicitly deselect streams not in test_catalogs.
        
        CHANGE REASON:
        The test_all_fields and test_automatic_fields tests were failing with errors like:
        "Stream X selected, but not testable" for streams not in streams_to_test().
        
        ORIGINAL ISSUE:
        The base test framework passes only a subset of catalogs (test_catalogs) to
        select_streams_and_fields(), expecting that ONLY those streams will be selected.
        However, in the tap-tester in_memory backend, streams that are not explicitly
        deselected remain in their default state, which may be "selected=True".
        
        EXAMPLE OF FAILURE:
        - streams_to_test() returns: {"metrics_time_series"}
        - test_catalogs contains only: metrics_time_series catalog
        - But discovered catalog has: all 32 streams
        - After selection, ALL 32 streams are still selected
        - Test assertion fails: "Stream 'events' selected, but not testable"
        
        SOLUTION:
        Before selecting test_catalogs, explicitly iterate through ALL discovered
        catalogs and set selected=False for any stream NOT in test_catalogs.
        This ensures a clean slate where only the intended test streams are selected.
        
        IMPLEMENTATION DETAILS:
        1. Get all discovered catalogs from menagerie
        2. Extract stream names from test_catalogs
        3. For each catalog NOT in test_catalogs:
           - Get the annotated schema for that stream
           - Create metadata with selected=False
           - Apply this metadata using select_catalog_and_fields_via_metadata()
        4. Call parent method to select and verify the test catalogs
        
        EXAMPLE:
        Test wants to run on: ["metrics_time_series"]
        Discovered streams: ["events", "webhooks", "metrics_time_series", ...]
        
        Step 1: Deselect "events", "webhooks", etc. (set selected=False)
        Step 2: Select "metrics_time_series" (set selected=True + fields)
        Result: Only "metrics_time_series" is selected and synced
        """
        # Get all discovered catalogs
        all_catalogs = menagerie.get_catalogs(conn_id)
        test_stream_names = {tc.get('stream_name') for tc in test_catalogs}
        
        # Explicitly deselect streams NOT in test_catalogs
        for catalog in all_catalogs:
            if catalog.get('stream_name') not in test_stream_names:
                schema = menagerie.get_annotated_schema(conn_id, catalog['stream_id'])
                # Set selected=False in metadata for this stream
                non_selected_metadata = [
                    {"breadcrumb": [], "metadata": {'selected': False}}
                ]
                connections.select_catalog_and_fields_via_metadata(
                    conn_id, catalog, schema, additional_md=non_selected_metadata
                )
        
        # Now call the parent method to select and verify the test catalogs
        super().perform_and_verify_table_and_field_selection(conn_id, test_catalogs)
