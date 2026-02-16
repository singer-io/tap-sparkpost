"""Account stream for SparkPost tap."""
# pylint: disable=duplicate-code
from tap_sparkpost.streams.abstracts import FullTableStream

class Account(FullTableStream):
    """Stream for retrieving account information."""
    tap_stream_id = "account"
    key_properties = ["customer_id"]
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "account"

    def get_records(self):
        """Account endpoint returns a single object, not an array."""
        response = self.client.make_request(
            method=self.http_method,
            endpoint=self.url_endpoint,
            params=self.params,
            headers=self.headers,
            path=self.path
        )

        data = response.get(self.data_key)
        if data:
            yield data
