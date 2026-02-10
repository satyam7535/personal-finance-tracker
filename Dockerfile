# Multi-stage Dockerfile for Finance Tracker Django Application
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 django && \
    mkdir -p /app /app/staticfiles /app/media && \
    chown -R django:django /app

WORKDIR /app

# Install Python dependencies
COPY --chown=django:django requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=django:django . .

# Create necessary directories with proper permissions
RUN mkdir -p staticfiles media && \
    chown -R django:django staticfiles media

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Make entrypoint script executable
USER root
RUN chmod +x docker-entrypoint.sh
USER django

# Set entrypoint
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Default command
CMD ["gunicorn", "finance_tracker.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
