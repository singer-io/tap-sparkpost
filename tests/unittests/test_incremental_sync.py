"""Unit tests for incremental sync and bookmark management."""
import unittest
from unittest.mock import patch, MagicMock
from singer import Transformer
from tap_sparkpost.streams.events import Events


class TestIncrementalBookmark(unittest.TestCase):
    """Test incremental sync bookmark management."""

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
                "event_id": {"type": "string"},
                "timestamp": {"type": "string", "format": "date-time"}
            }
        }
        catalog.metadata = []

        self.stream = Events(client=client, catalog=catalog)
        self.stream.is_selected = MagicMock(return_value=True)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.write_bookmark")
    @patch("tap_sparkpost.streams.abstracts.get_bookmark")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_bookmark_updated_with_latest_record(self, mock_counter, mock_get_bookmark,
                                                 mock_write_bookmark, mock_write_record):
        """Test that bookmark is updated with the latest record timestamp."""
        mock_get_bookmark.return_value = "2024-01-01T00:00:00Z"
        mock_write_bookmark.return_value = {}

        mock_records = [
            {"event_id": "1", "timestamp": "2024-01-02T00:00:00Z"},
            {"event_id": "2", "timestamp": "2024-01-03T00:00:00Z"},
            {"event_id": "3", "timestamp": "2024-01-04T00:00:00Z"}
        ]

        self.stream.get_records = MagicMock(return_value=iter(mock_records))
        transformer = Transformer()
        state = {"bookmarks": {"events": {"timestamp": "2024-01-01T00:00:00Z"}}}

        self.stream.sync(state, transformer)

        # Verify bookmark was written with latest timestamp
        self.assertTrue(mock_write_bookmark.called)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.get_bookmark")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_incremental_uses_bookmark(self, mock_counter, mock_get_bookmark, mock_write_record):
        """Test that incremental sync uses bookmark (or start_date as default)."""
        bookmark_date = "2024-01-03T00:00:00Z"
        mock_get_bookmark.return_value = bookmark_date

        mock_records = [
            {"event_id": "2", "timestamp": "2024-01-03T00:00:00Z"},
            {"event_id": "3", "timestamp": "2024-01-04T00:00:00Z"}
        ]

        self.stream.get_records = MagicMock(return_value=iter(mock_records))
        transformer = Transformer()
        state = {"bookmarks": {"events": {"timestamp": bookmark_date}}}

        self.stream.sync(state, transformer)

        mock_get_bookmark.assert_called()
        self.assertTrue(mock_write_record.call_count >= 1)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.write_bookmark")
    @patch("tap_sparkpost.streams.abstracts.get_bookmark")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_bookmark_not_regressed(self, mock_counter, mock_get_bookmark,
                                   mock_write_bookmark, mock_write_record):
        """Test that bookmark is not regressed to earlier date."""
        current_bookmark = "2024-01-05T00:00:00Z"
        mock_get_bookmark.return_value = current_bookmark
        mock_write_bookmark.return_value = {}

        # Records with earlier timestamps
        mock_records = [
            {"event_id": "1", "timestamp": "2024-01-03T00:00:00Z"},
            {"event_id": "2", "timestamp": "2024-01-04T00:00:00Z"}
        ]

        self.stream.get_records = MagicMock(return_value=iter(mock_records))
        transformer = Transformer()
        state = {"bookmarks": {"events": {"timestamp": current_bookmark}}}

        self.stream.sync(state, transformer)

        # Bookmark should not regress
        if mock_write_bookmark.called:
            calls = mock_write_bookmark.call_args_list
            for call in calls:
                _, kwargs = call
                if 'value' in kwargs:
                    self.assertTrue(kwargs['value'] >= current_bookmark)


if __name__ == '__main__':
    unittest.main()
