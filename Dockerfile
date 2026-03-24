# Use official Python slim image for smaller size
FROM python:3.12-slim-bookworm AS app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create a non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

# Set work directory
WORKDIR /app

# Install system dependencies if needed (none currently)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Ensure cache directory exists and has correct permissions
RUN mkdir -p /home/appuser/.cache && chown -R appuser:appuser /home/appuser/.cache

# Switch to non-root user
USER appuser

# Expose ports (used by services in docker-compose)
EXPOSE 8000 8501

# Default command (overridden in docker-compose.yml)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
