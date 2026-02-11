"""Metrics Time Series stream for SparkPost tap."""
import singer
from tap_sparkpost.streams.abstracts import MetricsBaseStream

LOGGER = singer.get_logger()


class MetricsTimeSeries(MetricsBaseStream):
    """Stream for retrieving time series metrics.

    This is the ONLY metrics endpoint that supports the 'precision' parameter.
    Reference:
    https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics

    Precision controls aggregation level: 1min, 5min, 15min, hour, 12hr,
    day, week, month
    """
    tap_stream_id = "metrics_time_series"
    key_properties = ["timestamp"]
    data_key = "results"
    path = "metrics/deliverability/time-series"

    def __init__(self, client=None, catalog=None, config=None) -> None:
        """Initialize MetricsTimeSeries with precision parameter.

        Args:
            client: API client instance
            catalog: Stream catalog
            config: Configuration dict with optional 'precision' parameter

        Precision values (default: 'day'):
            - '1min': 1-minute aggregation
            - '5min': 5-minute aggregation
            - '15min': 15-minute aggregation
            - 'hour': Hourly aggregation
            - '12hr': 12-hour aggregation
            - 'day': Daily aggregation (default)
            - 'week': Weekly aggregation
            - 'month': Monthly aggregation

        Reference:
        https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics

        Note: Precision MUST NOT change during a sync to prevent
        mixed aggregation records in the same dataset.
        """
        super().__init__(client, catalog, config)

        # Get aggregation precision from config, default to 'day'
        self.precision = self.config.get('precision', 'day')

        # Validate precision against SparkPost API allowed values
        valid_precisions = [
            '1min', '5min', '15min', 'hour', '12hr',
            'day', 'week', 'month'
        ]

        if self.precision not in valid_precisions:
            LOGGER.warning(
                "Invalid precision '%s'. Using default 'day'. "
                "Valid values: %s",
                self.precision, valid_precisions
            )
            self.precision = 'day'

    def get_precision_params(self):
        """Return precision parameter for time-series API request.

        Returns:
            Dict: {'precision': value} for time-series endpoint

        Note:
            This overrides the base class method which returns empty dict.
            Precision is ONLY valid for time-series endpoint per SparkPost API.
        """
        return {"precision": self.precision}
