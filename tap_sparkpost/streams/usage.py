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

        # Usage endpoint returns: {results: {messaging: {day: {}, month: {}, timestamp: "..."},
        #                                     recipient_validation: {...}}}
        # Yield a flat record matching the schema with top-level messaging and recipient_validation.
        results = response.get(self.data_key, {})
        if results:
            record = {
                "timestamp": results.get("messaging", {}).get("timestamp"),
                "messaging": results.get("messaging"),
                "recipient_validation": results.get("recipient_validation"),
            }
            yield record
