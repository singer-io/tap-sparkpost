"""Unit tests for discovery flow."""
import unittest
from tap_sparkpost.discover import discover


class TestDiscoveryFlow(unittest.TestCase):
    """Test discovery flow and catalog generation."""

    def test_discover_returns_catalog(self):
        """Test that discover returns a valid catalog."""
        catalog = discover()

        # Should return a catalog object
        self.assertIsNotNone(catalog)
        self.assertTrue(hasattr(catalog, 'streams'))

    def test_discover_includes_streams(self):
        """Test that streams are included in catalog."""
        catalog = discover()

        # Should include streams
        stream_ids = [stream.tap_stream_id for stream in catalog.streams]
        
        # Check that major streams are present
        expected_streams = ['events', 'webhooks', 'templates', 'account']
        for stream in expected_streams:
            self.assertIn(stream, stream_ids)

    def test_discover_stream_has_schema(self):
        """Test that discovered streams have schemas."""
        catalog = discover()

        # Each stream should have a schema
        for stream in catalog.streams:
            self.assertIsNotNone(stream.schema)
            self.assertTrue(hasattr(stream.schema, 'to_dict'))

    def test_discover_stream_has_metadata(self):
        """Test that discovered streams have metadata."""
        catalog = discover()

        # Each stream should have metadata
        for stream in catalog.streams:
            self.assertIsNotNone(stream.metadata)
            self.assertIsInstance(stream.metadata, list)

    def test_discover_stream_has_key_properties(self):
        """Test that discovered streams have key_properties."""
        catalog = discover()

        # Each stream should have key_properties
        for stream in catalog.streams:
            self.assertIsNotNone(stream.key_properties)
            self.assertIsInstance(stream.key_properties, list)

    def test_discover_streams_have_replication_method(self):
        """Test that streams have forced-replication-method in metadata."""
        catalog = discover()

        # Check streams have forced-replication-method (Singer standard)
        for stream in catalog.streams:
            # Singer metadata uses tuples for breadcrumbs, not lists
            root_metadata = [m for m in stream.metadata if m.get('breadcrumb') == () or m.get('breadcrumb') == []]
            self.assertTrue(len(root_metadata) > 0, f"Stream {stream.tap_stream_id} has no root metadata")
            if root_metadata:
                metadata_dict = root_metadata[0].get('metadata', {})
                self.assertIn('forced-replication-method', metadata_dict,
                             f"Stream {stream.tap_stream_id} missing forced-replication-method")
                self.assertIn(metadata_dict['forced-replication-method'], ['INCREMENTAL', 'FULL_TABLE'],
                             f"Stream {stream.tap_stream_id} has invalid forced-replication-method: {metadata_dict.get('forced-replication-method')}")

