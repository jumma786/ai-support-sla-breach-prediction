# SLA Breach Prediction API
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and training data
COPY src/ src/
COPY scripts/ scripts/
COPY main.py .
COPY ["01_Data/processed data/model_ready_support_sla_sample.csv", "01_Data/processed data/"]

# Train the model at build time (model file is not stored in git)
RUN python scripts/train_model.py

# Run as non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Healthcheck without curl (not present in slim image)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://localhost:{os.environ.get(\"PORT\", \"8000\")}/health')" || exit 1

# Bind to $PORT when provided (Render/Heroku style), default 8000
CMD uvicorn src.api.app:create_app --factory --host 0.0.0.0 --port ${PORT:-8000}
