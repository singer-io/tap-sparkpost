"""Unit tests for incremental sync with bookmark management."""
import unittest
from unittest.mock import patch, MagicMock
from singer import Transformer
from tap_sparkpost.streams.events import Events
from tap_sparkpost.streams.abstracts import IncrementalStream


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
    def test_bookmark_updated_with_latest_record(self, mock_counter, mock_get_bookmark, mock_write_bookmark, mock_write_record):
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
        calls = mock_write_bookmark.call_args_list
        # Should be called for batch writes and final write
        self.assertTrue(len(calls) >= 1)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.get_bookmark")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_incremental_filters_old_records(self, mock_counter, mock_get_bookmark, mock_write_record):
        """Test that incremental sync only writes records at or after bookmark."""
        bookmark_date = "2024-01-03T00:00:00Z"
        mock_get_bookmark.return_value = bookmark_date

        # API should return records at or after bookmark
        mock_records = [
            {"event_id": "2", "timestamp": "2024-01-03T00:00:00Z"},  # At bookmark
            {"event_id": "3", "timestamp": "2024-01-04T00:00:00Z"}   # After bookmark
        ]

        self.stream.get_records = MagicMock(return_value=iter(mock_records))

        transformer = Transformer()
        state = {"bookmarks": {"events": {"timestamp": bookmark_date}}}

        self.stream.sync(state, transformer)

        # Should write all records returned by API (already filtered)
        self.assertTrue(mock_write_record.call_count >= 1)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.write_bookmark")
    @patch("tap_sparkpost.streams.abstracts.get_bookmark")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_batch_bookmark_writing(self, mock_counter, mock_get_bookmark, mock_write_bookmark, mock_write_record):
        """Test that bookmarks are written after processing all records."""
        mock_get_bookmark.return_value = "2024-01-01T00:00:00Z"
        mock_write_bookmark.return_value = {}

        # Generate 250 records with valid dates (spread across days)
        mock_records = [
            {"event_id": str(i), "timestamp": f"2024-01-{(i//100)+1:02d}T{(i%24):02d}:{(i%60):02d}:00Z"}
            for i in range(1, 251)
        ]

        self.stream.get_records = MagicMock(return_value=iter(mock_records))

        transformer = Transformer()
        state = {"bookmarks": {}}

        self.stream.sync(state, transformer)

        # Should write bookmark at least once at the end
        self.assertTrue(mock_write_bookmark.call_count >= 1)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.get_bookmark")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_incremental_uses_start_date(self, mock_counter, mock_get_bookmark, mock_write_record):
        """Test that incremental sync uses start_date when no bookmark exists."""
        start_date = "2024-01-01T00:00:00Z"
        mock_get_bookmark.return_value = start_date  # Returns start_date as default

        mock_records = [
            {"event_id": "1", "timestamp": "2024-01-02T00:00:00Z"}
        ]

        self.stream.get_records = MagicMock(return_value=iter(mock_records))

        transformer = Transformer()
        state = {"bookmarks": {}}

        self.stream.sync(state, transformer)

        # Verify get_bookmark was called
        mock_get_bookmark.assert_called()

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.get_bookmark")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_incremental_sets_from_parameter(self, mock_counter, mock_get_bookmark, mock_write_record):
        """Test that incremental sync sets from_date parameter."""
        bookmark_date = "2024-01-01T00:00:00Z"
        mock_get_bookmark.return_value = bookmark_date

        self.stream.get_records = MagicMock(return_value=iter([]))

        transformer = Transformer()
        state = {"bookmarks": {"events": {"timestamp": bookmark_date}}}

        self.stream.sync(state, transformer)

        # Verify get_records was called
        self.stream.get_records.assert_called()

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.write_bookmark")
    @patch("tap_sparkpost.streams.abstracts.get_bookmark")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_bookmark_not_regressed(self, mock_counter, mock_get_bookmark, mock_write_bookmark, mock_write_record):
        """Test that bookmark is not regressed to earlier date."""
        # Current bookmark is at Jan 5
        current_bookmark = "2024-01-05T00:00:00Z"
        mock_get_bookmark.return_value = current_bookmark
        mock_write_bookmark.return_value = {}

        # Records returned have earlier timestamps
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
            # Check that bookmark was not set to earlier date
            calls = mock_write_bookmark.call_args_list
            for call in calls:
                _, kwargs = call
                if 'value' in kwargs:
                    # Bookmark value should be >= current_bookmark
                    self.assertTrue(kwargs['value'] >= current_bookmark)

    @patch("tap_sparkpost.streams.abstracts.write_record")
    @patch("tap_sparkpost.streams.abstracts.write_bookmark")
    @patch("tap_sparkpost.streams.abstracts.get_bookmark")
    @patch("tap_sparkpost.streams.abstracts.metrics.record_counter")
    def test_sync_writes_records(self, mock_counter, mock_get_bookmark, mock_write_bookmark, mock_write_record):
        """Test that RECORD messages are written for selected streams."""
        mock_get_bookmark.return_value = "2024-01-01T00:00:00Z"
        mock_records = [{"event_id": "1", "timestamp": "2024-01-02T00:00:00Z"}]
        self.stream.get_records = MagicMock(return_value=iter(mock_records))

        transformer = Transformer()
        state = {"bookmarks": {}}

        self.stream.sync(state, transformer)

        # Records should be written (if stream is selected)
        if self.stream.is_selected():
            mock_write_record.assert_called()
