"""Metrics Time Series stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsTimeSeries(MetricsBaseStream):
    """Stream for retrieving time series metrics."""
    tap_stream_id = "metrics_time_series"
    key_properties = ["ts"]
    data_key = "results"
    path = "metrics/deliverability/time-series"
