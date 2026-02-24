"""Usage stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import FullTableStream

class Usage(FullTableStream):
    """Stream for retrieving usage statistics."""
    tap_stream_id = "usage"
    key_properties = ["timestamp"]
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "usage"

    def get_records(self):
        """Override to handle usage endpoint returning nested object structure"""
        response = self.client.make_request(
            method=self.http_method,
            endpoint=self.url_endpoint,
            params=self.params,
            headers=self.headers,
            path=self.path
        )

        # Usage endpoint returns nested structure: {results: {messaging: {...}, recipient_validation: {...}}}
        # Spread top-level fields directly so the record matches the schema
        results = response.get(self.data_key, {})
        if results:
            record = {
                "timestamp": results.get("messaging", {}).get("day", {}).get("start"),
                "messaging": results.get("messaging"),
                "recipient_validation": results.get("recipient_validation"),
            }
            if record["timestamp"]:
                yield record
