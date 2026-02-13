"""Unit tests for sync flow, bookmarking, and precision parameter."""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from tap_sparkpost.sync import write_schema, sync, update_currently_syncing
from tap_sparkpost.streams.metrics_time_series import MetricsTimeSeries
from tap_sparkpost.streams.metrics_campaign import MetricsCampaign


class TestSyncFlow(unittest.TestCase):
    """Test sync flow and schema writing."""

    def test_write_schema_stream_selected(self):
        """Test write_schema when stream is selected."""
        mock_stream = MagicMock()
        mock_stream.is_selected.return_value = True
        mock_stream.children = []
        mock_stream.child_to_sync = []

        client = MagicMock()
        catalog = MagicMock()
        catalog.get_stream.return_value = MagicMock()
        config = {}

        write_schema(mock_stream, client, [], catalog, config)

        mock_stream.write_schema.assert_called_once()
        self.assertEqual(len(mock_stream.child_to_sync), 0)

    def test_write_schema_stream_not_selected(self):
        """Test write_schema when stream is not selected."""
        mock_stream = MagicMock()
        mock_stream.is_selected.return_value = False
        mock_stream.children = []
        mock_stream.child_to_sync = []

        client = MagicMock()
        catalog = MagicMock()
        catalog.get_stream.return_value = MagicMock()
        config = {}

        write_schema(mock_stream, client, [], catalog, config)

        self.assertEqual(mock_stream.write_schema.call_count, 0)
        self.assertEqual(len(mock_stream.child_to_sync), 0)

    @patch("singer.write_schema")
    @patch("singer.get_currently_syncing")
    @patch("singer.Transformer")
    @patch("singer.write_state")
    @patch("tap_sparkpost.streams.abstracts.IncrementalStream.sync")
    def test_sync_multiple_streams_called(self, mock_sync, mock_write_state, mock_transformer,
                                         mock_get_currently_syncing, mock_write_schema):
        """Test that sync is called for each selected stream."""
        mock_catalog = MagicMock()
        events_stream = MagicMock()
        events_stream.stream = "events"
        webhooks_stream = MagicMock()
        webhooks_stream.stream = "webhooks"
        mock_catalog.get_selected_streams.return_value = [events_stream, webhooks_stream]
        state = {}

        client = MagicMock()
        config = {}

        sync(client, config, mock_catalog, state)

        self.assertEqual(mock_sync.call_count, 2)

    @patch("singer.get_currently_syncing")
    @patch("singer.set_currently_syncing")
    @patch("singer.write_state")
    def test_remove_currently_syncing(self, mock_write_state, mock_set_currently_syncing,
                                     mock_get_currently_syncing):
        """Test removing currently_syncing from state."""
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
    def test_set_currently_syncing(self, mock_write_state, mock_set_currently_syncing,
                                  mock_get_currently_syncing):
        """Test setting currently_syncing in state."""
        mock_get_currently_syncing.return_value = None
        state = {}

        update_currently_syncing(state, "new_stream")

        mock_get_currently_syncing.assert_not_called()
        mock_set_currently_syncing.assert_called_once_with(state, "new_stream")
        mock_write_state.assert_called_once_with(state)
        self.assertNotIn("currently_syncing", state)


class TestPrecisionParameter(unittest.TestCase):
    """Test precision parameter for metrics_time_series stream."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = MagicMock()
        self.mock_catalog = MagicMock()

    def test_precision_default_value(self):
        """Test that precision defaults to 'day' when not specified."""
        config = {}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, 'day')
        params = stream.get_precision_params()
        self.assertEqual(params, {'precision': 'day'})

    @parameterized.expand([
        ['1min'],
        ['5min'],
        ['15min'],
        ['hour'],
        ['12hr'],
        ['day'],
        ['week'],
        ['month']
    ])
    def test_precision_valid_values(self, precision_value):
        """Test that all valid precision values are accepted."""
        config = {'precision': precision_value}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, precision_value)
        params = stream.get_precision_params()
        self.assertEqual(params, {'precision': precision_value})

    @patch('tap_sparkpost.streams.metrics_time_series.LOGGER')
    def test_precision_invalid_value_fallback(self, mock_logger):
        """Test that invalid precision logs warning and defaults to 'day'."""
        config = {'precision': 'invalid_value'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, 'day')
        mock_logger.warning.assert_called_once()
        warning_call = mock_logger.warning.call_args
        self.assertIn('Invalid precision', warning_call[0][0])

    def test_other_metrics_streams_no_precision(self):
        """Test that other metrics streams don't have precision parameter."""
        config = {'precision': 'hour'}
        stream = MetricsCampaign(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        params = stream.get_precision_params()
        self.assertEqual(params, {})


if __name__ == '__main__':
    unittest.main() 
