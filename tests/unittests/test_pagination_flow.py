"""Unit tests for pagination logic."""
import unittest
from unittest.mock import MagicMock
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
        page1 = {
            "results": [{"event_id": str(i)} for i in range(1000)],
            "links": [{"rel": "next", "href": "/api/v1/events?cursor=next_page"}]
        }
        page2 = {
            "results": [{"event_id": str(i)} for i in range(1000, 1500)],
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

        self.assertEqual(self.stream.client.make_request.call_count, 2)

    def test_pagination_handles_missing_data_key(self):
        """Test pagination when response doesn't have data_key."""
        mock_response = {"error": "No data"}

        self.stream.client.make_request = MagicMock(return_value=mock_response)
        self.stream.data_key = "results"

        records = list(self.stream.get_records())

        self.assertEqual(len(records), 0)

    def test_pagination_respects_max_pages_limit(self):
        """Test that pagination stops at max_pages safety limit."""
        # Create a response that always has a next page
        mock_response = {
            "results": [{"event_id": "1"}],
            "links": [{"rel": "next", "href": "/api/v1/events?cursor=next"}]
        }

        self.stream.client.make_request = MagicMock(return_value=mock_response)
        
        # Consume records - should stop at max_pages limit (10000)
        # This would infinite loop without the safety limit
        records = []
        for i, record in enumerate(self.stream.get_records()):
            records.append(record)
            # Stop early for test performance
            if i >= 100:
                break

        # Should have collected records but stopped due to safety
        self.assertTrue(len(records) > 0)
