"""Unit tests for full table sync behavior."""
import unittest
from unittest.mock import patch, MagicMock
from singer import Transformer
from tap_sparkpost.streams.account import Account


class TestFullTableSync(unittest.TestCase):
    """Test full table sync behavior."""

    def setUp(self):
        """Set up test stream."""
        config = {
            "api_key": "test_key",
            "start_date": "2024-01-01T00:00:00Z",
            "base_url": "https://api.sparkpost.com/api/v1"
        }
        client = MagicMock()
        client.config = config

        catalog = MagicMock()
        catalog.schema.to_dict.return_value = {
            "type": "object",
            "properties": {
                "customer_id": {"type": "integer"}
            }
        }
        catalog.metadata = []

        self.stream = Account(client=client, catalog=catalog)
        self.stream.is_selected = MagicMock(return_value=True)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_full_table_no_bookmark(self, mock_counter, mock_write_record):
        """Test that FULL_TABLE streams don't use bookmarks."""
        mock_records = [
            {"customer_id": 100},
            {"customer_id": 200}
        ]

        self.stream.get_records = MagicMock(return_value=iter(mock_records))

        transformer = Transformer()
        state = {}

        self.stream.sync(state, transformer)

        # Should write all records
        self.assertEqual(mock_write_record.call_count, 2)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_full_table_ignores_existing_bookmark(self, mock_counter, mock_write_record):
        """Test that FULL_TABLE streams ignore existing bookmarks."""
        mock_records = [
            {"customer_id": 300}
        ]

        self.stream.get_records = MagicMock(return_value=iter(mock_records))

        transformer = Transformer()
        # State has bookmarks, but FULL_TABLE should ignore them
        state = {"bookmarks": {"account": {"timestamp": "2024-01-01T00:00:00Z"}}}

        self.stream.sync(state, transformer)

        # Should still write all records
        self.assertEqual(mock_write_record.call_count, 1)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_full_table_syncs_all_data(self, mock_counter, mock_write_record):
        """Test that FULL_TABLE syncs all data every time."""
        mock_records = [{"customer_id": i} for i in range(50)]

        self.stream.get_records = MagicMock(return_value=iter(mock_records))

        transformer = Transformer()
        state = {}

        self.stream.sync(state, transformer)

        # Should write all 50 records
        self.assertEqual(mock_write_record.call_count, 50)
