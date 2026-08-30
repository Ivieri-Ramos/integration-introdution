FROM python:3.12-slim AS python-dev

RUN pip uninstall -y pip setuptools wheel

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && \
    apt-get install -y git curl && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash devuser && \
    mkdir -p /opt/venv /app && \
    chown -R devuser:devuser /opt/venv /app

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT="/opt/venv" \
    PATH="/opt/venv/bin:$PATH"
