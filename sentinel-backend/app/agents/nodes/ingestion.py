# app/nodes/ingest_vendor.py

import time
from app.observability.logging import logger
from app.observability.metrics import record_vendor_run, observe_latency
from app.observability.tracing import start_span

logger.info("Running retrieval node")

async def ingest_vendor(state: dict) -> dict:
    """
    Entry node.
    Ensures required fields exist and normalizes state.
    """

    start = time.time()

    # Wrap node execution in a trace span
    with start_span("ingest_vendor"):
        # Structured log with context
        logger.info("ingest_vendor.start", extra={
            "node": "ingest_vendor",
            "vendor_id": state.get("vendor_id"),
        })

        # Increment Prometheus counter
        record_vendor_run()

        # --- existing functionality preserved ---
        result = {
            "vendor_id": state["vendor_id"],
            "vendor_name": state.get("vendor_name", "Unknown Vendor"),
            "retrieved_docs": [],
            "final_assessment": "",
        }

        logger.info("ingest_vendor.complete", extra={
            "node": "ingest_vendor",
            "vendor_id": state.get("vendor_id"),
            "result_keys": list(result.keys()),
        })

    # Record latency metric
    observe_latency("ingest_vendor", time.time() - start)

    return result