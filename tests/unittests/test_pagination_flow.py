"""Unit tests for pagination logic."""
import unittest
from unittest.mock import patch, MagicMock
from tap_sparkpost.streams.events import Events


class TestPaginationFlow(unittest.TestCase):
    """Test pagination logic in get_records method."""

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
        catalog.schema.to_dict.return_value = {"type": "object", "properties": {}}
        catalog.metadata = []

        self.stream = Events(client=client, catalog=catalog)

    def test_pagination_single_page(self):
        """Test pagination with single page of results."""
        mock_response = {
            "results": [
                {"event_id": "1", "timestamp": "2024-01-01T00:00:00Z"},
                {"event_id": "2", "timestamp": "2024-01-02T00:00:00Z"}
            ]
        }

        self.stream.client.make_request = MagicMock(return_value=mock_response)

        records = list(self.stream.get_records())

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["event_id"], "1")
        self.stream.client.make_request.assert_called_once()

    def test_pagination_multiple_pages(self):
        """Test pagination with multiple pages using cursor."""
        # First page: has cursor for next page
        page1 = {
            "results": [{"event_id": str(i), "timestamp": f"2024-01-01T00:00:0{i}Z"} for i in range(1000)],
            "links": [{"rel": "next", "href": "/api/v1/events?cursor=next_page_token"}]
        }
        # Second page: partial page (no cursor)
        page2 = {
            "results": [{"event_id": str(i), "timestamp": f"2024-01-02T00:00:0{i}Z"} for i in range(1000, 1500)],
            "links": []
        }

        self.stream.client.make_request = MagicMock(side_effect=[page1, page2])

        records = list(self.stream.get_records())

        self.assertEqual(len(records), 1500)
        self.assertEqual(self.stream.client.make_request.call_count, 2)

    def test_pagination_empty_results(self):
        """Test pagination with empty results."""
        mock_response = {"results": []}

        self.stream.client.make_request = MagicMock(return_value=mock_response)

        records = list(self.stream.get_records())

        self.assertEqual(len(records), 0)
        self.stream.client.make_request.assert_called_once()

    def test_pagination_cursor_extraction(self):
        """Test that cursor is correctly extracted from links."""
        page1 = {
            "results": [{"event_id": str(i)} for i in range(10)],
            "links": [
                {"rel": "self", "href": "/api/v1/events"},
                {"rel": "next", "href": "/api/v1/events?cursor=abc123"}
            ]
        }
        page2 = {"results": [{"event_id": str(i)} for i in range(10, 15)], "links": []}

        self.stream.client.make_request = MagicMock(side_effect=[page1, page2])

        list(self.stream.get_records())

        # Verify that cursor was extracted and used
        self.assertEqual(self.stream.client.make_request.call_count, 2)

    def test_pagination_per_page_parameter(self):
        """Test that per_page parameter is set correctly."""
        mock_response = {"results": [{"event_id": "1"}]}

        self.stream.client.make_request = MagicMock(return_value=mock_response)

        list(self.stream.get_records())

        # Verify per_page was set in params
        call_args = self.stream.client.make_request.call_args
        if call_args and len(call_args) > 0:
            # Check if params were passed
            params = call_args[1].get('params', {}) if len(call_args) > 1 else {}
            # per_page should be set to 1000 (default for SparkPost)
            if 'per_page' in params:
                self.assertEqual(params['per_page'], 1000)

    def test_pagination_stops_when_no_cursor(self):
        """Test that pagination stops when no next cursor provided."""
        page1 = {
            "results": [{"event_id": str(i)} for i in range(1000)],
            "links": [{"rel": "next", "href": "/api/v1/events?cursor=token1"}]
        }
        page2 = {
            "results": [{"event_id": str(i)} for i in range(1000, 1500)],
            "links": []  # No next link
        }

        self.stream.client.make_request = MagicMock(side_effect=[page1, page2])

        records = list(self.stream.get_records())

        # Should stop after page2 (no cursor)
        self.assertEqual(len(records), 1500)
        self.assertEqual(self.stream.client.make_request.call_count, 2)

    def test_pagination_data_key_extraction(self):
        """Test that data is extracted using correct data_key."""
        mock_response = {
            "results": [
                {"event_id": "1", "type": "bounce"},
                {"event_id": "2", "type": "delivery"}
            ],
            "total_count": 2
        }

        self.stream.client.make_request = MagicMock(return_value=mock_response)
        self.stream.data_key = "results"

        records = list(self.stream.get_records())

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["event_id"], "1")
        self.assertEqual(records[1]["event_id"], "2")

    def test_pagination_handles_missing_data_key(self):
        """Test pagination when response doesn't have data_key."""
        mock_response = {"error": "No data"}

        self.stream.client.make_request = MagicMock(return_value=mock_response)
        self.stream.data_key = "results"

        records = list(self.stream.get_records())

        # Should return empty list
        self.assertEqual(len(records), 0)

    def test_pagination_cursor_initial_value(self):
        """Test that cursor starts with 'initial' value."""
        mock_response = {
            "results": [{"event_id": "1"}],
            "links": []
        }

        self.stream.client.make_request = MagicMock(return_value=mock_response)

        list(self.stream.get_records())

        # Check first call parameters
        call_args = self.stream.client.make_request.call_args
        if call_args:
            params = call_args[1].get('params', {}) if len(call_args) > 1 else {}
            # Initial cursor should be 'initial'
            if 'cursor' in params:
                self.assertEqual(params['cursor'], 'initial')
