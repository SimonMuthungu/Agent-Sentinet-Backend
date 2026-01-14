# observability/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Set up tracer provider
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())  # prints spans to console
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("sentinel")

def start_span(name: str):
    """Context manager for tracing spans."""
    return tracer.start_as_current_span(name)

# Example usage in a node:
# from observability.tracing import start_span
# with start_span("human_review"):
#     ... node logic ...