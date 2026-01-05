FROM python:3.10-slim

WORKDIR /app

# Install dependencies
# Note: In a real production environment, you would use a lock file (poetry.lock, pdm.lock, etc.)
COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
