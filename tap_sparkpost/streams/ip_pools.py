"""IP Pools stream for SparkPost tap."""
from tap_sparkpost.streams.abstracts import FullTableStream

class IpPools(FullTableStream):
    """Stream for retrieving IP pool configurations."""
    tap_stream_id = "ip_pools"
    key_properties = ["id"]
    replication_method = "FULL_TABLE"
    data_key = "results"
    path = "ip-pools"
