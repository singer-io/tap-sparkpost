"""Unit tests for precision parameter functionality."""
import unittest
from unittest.mock import MagicMock, patch
from tap_sparkpost.streams.metrics_time_series import MetricsTimeSeries
from tap_sparkpost.streams.metrics_campaign import MetricsCampaign


class TestPrecisionParameter(unittest.TestCase):
    """Test precision parameter for MetricsTimeSeries stream."""

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

    def test_precision_valid_1min(self):
        """Test that precision accepts valid value '1min'."""
        config = {'precision': '1min'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, '1min')

    def test_precision_valid_5min(self):
        """Test that precision accepts valid value '5min'."""
        config = {'precision': '5min'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, '5min')

    def test_precision_valid_15min(self):
        """Test that precision accepts valid value '15min'."""
        config = {'precision': '15min'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, '15min')

    def test_precision_valid_hour(self):
        """Test that precision accepts valid value 'hour'."""
        config = {'precision': 'hour'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, 'hour')

    def test_precision_valid_12hr(self):
        """Test that precision accepts valid value '12hr'."""
        config = {'precision': '12hr'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, '12hr')

    def test_precision_valid_day(self):
        """Test that precision accepts valid value 'day'."""
        config = {'precision': 'day'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, 'day')

    def test_precision_valid_week(self):
        """Test that precision accepts valid value 'week'."""
        config = {'precision': 'week'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, 'week')

    def test_precision_valid_month(self):
        """Test that precision accepts valid value 'month'."""
        config = {'precision': 'month'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        self.assertEqual(stream.precision, 'month')

    @patch('tap_sparkpost.streams.metrics_time_series.LOGGER')
    def test_precision_invalid_value(self, mock_logger):
        """Test that invalid precision logs warning and defaults to 'day'."""
        config = {'precision': 'invalid_value'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        # Should default to 'day'
        self.assertEqual(stream.precision, 'day')

        # Should log warning
        mock_logger.warning.assert_called_once()
        warning_call = mock_logger.warning.call_args
        self.assertIn('Invalid precision', warning_call[0][0])
        self.assertIn('invalid_value', warning_call[0][1])

    def test_get_precision_params_returns_dict(self):
        """Test that get_precision_params returns dict with precision."""
        config = {'precision': 'hour'}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        params = stream.get_precision_params()

        self.assertIsInstance(params, dict)
        self.assertIn('precision', params)
        self.assertEqual(params['precision'], 'hour')

    def test_get_precision_params_default(self):
        """Test that get_precision_params returns 'day' when not specified."""
        config = {}
        stream = MetricsTimeSeries(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        params = stream.get_precision_params()

        self.assertEqual(params['precision'], 'day')

    def test_other_metrics_streams_no_precision(self):
        """Test that other metrics streams don't have precision parameter."""
        config = {'precision': 'hour'}
        stream = MetricsCampaign(
            client=self.mock_client,
            catalog=self.mock_catalog,
            config=config
        )

        # MetricsCampaign should not use precision
        params = stream.get_precision_params()

        # Should return empty dict (base class behavior)
        self.assertEqual(params, {})


if __name__ == '__main__':
    unittest.main()
