# observability/metrics.py
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Define metrics
vendor_runs_total = Counter("vendor_runs_total", "Total vendor runs processed")
escalations_total = Counter("escalations_total", "Total escalations created")
node_latency = Histogram("node_latency_seconds", "Latency per node", ["node"])

def start_metrics_server(port: int = 9000):
    """Start Prometheus metrics server."""
    start_http_server(port)

# Example usage in a node:
def record_vendor_run():
    vendor_runs_total.inc()

def record_escalation():
    escalations_total.inc()

def observe_latency(node_name: str, seconds: float):
    node_latency.labels(node=node_name).observe(seconds)