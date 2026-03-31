"""Metrics Template stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import MetricsBaseStream

class MetricsTemplate(MetricsBaseStream):
    """Stream for retrieving template metrics."""
    tap_stream_id = "metrics_template"
    key_properties = ["timestamp", "template_id"]
    data_key = "results"
    path = "metrics/deliverability/template"
