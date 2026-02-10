import unittest
from unittest.mock import patch, MagicMock
from tap_sparkpost.sync import write_schema, sync, update_currently_syncing

class TestSync(unittest.TestCase):

    def test_write_schema_stream_selected(self):
        """Test write_schema when stream is selected"""
        mock_stream = MagicMock()
        mock_stream.is_selected.return_value = True
        mock_stream.children = []
        mock_stream.child_to_sync = []

        client = MagicMock()
        catalog = MagicMock()
        catalog.get_stream.return_value = MagicMock()

        write_schema(mock_stream, client, [], catalog)

        mock_stream.write_schema.assert_called_once()
        self.assertEqual(len(mock_stream.child_to_sync), 0)

    def test_write_schema_stream_not_selected(self):
        """Test write_schema when stream is not selected"""
        mock_stream = MagicMock()
        mock_stream.is_selected.return_value = False
        mock_stream.children = []
        mock_stream.child_to_sync = []

        client = MagicMock()
        catalog = MagicMock()
        catalog.get_stream.return_value = MagicMock()

        write_schema(mock_stream, client, [], catalog)

        self.assertEqual(mock_stream.write_schema.call_count, 0)
        self.assertEqual(len(mock_stream.child_to_sync), 0)

    @patch("singer.write_schema")
    @patch("singer.get_currently_syncing")
    @patch("singer.Transformer")
    @patch("singer.write_state")
    @patch("tap_sparkpost.streams.abstracts.IncrementalStream.sync")
    def test_sync_multiple_streams_called(self, mock_sync, mock_write_state, mock_transformer, mock_get_currently_syncing, mock_write_schema):
        """Test that sync is called for each selected stream"""
        mock_catalog = MagicMock()
        events_stream = MagicMock()
        events_stream.stream = "events"
        webhooks_stream = MagicMock()
        webhooks_stream.stream = "webhooks"
        mock_catalog.get_selected_streams.return_value = [
            events_stream,
            webhooks_stream
        ]
        state = {}

        client = MagicMock()
        config = {}

        sync(client, config, mock_catalog, state)

        self.assertEqual(mock_sync.call_count, 2)

    @patch("singer.get_currently_syncing")
    @patch("singer.set_currently_syncing")
    @patch("singer.write_state")
    def test_remove_currently_syncing(self, mock_write_state, mock_set_currently_syncing, mock_get_currently_syncing):
        """Test removing currently_syncing from state"""
        mock_get_currently_syncing.return_value = "some_stream"
        state = {"currently_syncing": "some_stream"}

        update_currently_syncing(state, None)

        mock_get_currently_syncing.assert_called_once_with(state)
        mock_set_currently_syncing.assert_not_called()
        mock_write_state.assert_called_once_with(state)
        self.assertNotIn("currently_syncing", state) 

    @patch("singer.get_currently_syncing")
    @patch("singer.set_currently_syncing")
    @patch("singer.write_state")
    def test_set_currently_syncing(self, mock_write_state, mock_set_currently_syncing, mock_get_currently_syncing):
        """Test setting currently_syncing in state"""
        mock_get_currently_syncing.return_value = None
        state = {}

        update_currently_syncing(state, "new_stream")

        mock_get_currently_syncing.assert_not_called()
        mock_set_currently_syncing.assert_called_once_with(state, "new_stream")
        mock_write_state.assert_called_once_with(state)
        self.assertNotIn("currently_syncing", state) 
