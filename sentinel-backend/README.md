# Sentinel Backend

Sentinel is an agent-driven vendor risk and compliance platform designed for Fortune-1000-scale environments.

## Project Structure

This project follows a modular architecture:

- `app/api`: API endpoints and routers.
- `app/agents`: Agent definitions, graphs, and nodes.
- `app/domain`: Domain models, schemas, and events.
- `app/services`: External services integration (LLM, Vector Store, etc.).
- `app/persistence`: Database access and repositories.
- `app/observability`: Logging, tracing, and metrics.

## Getting Started

1. Install dependencies.
2. Run the application: `uvicorn app.main:app --reload`
