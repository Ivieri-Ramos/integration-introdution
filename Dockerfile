FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT="/opt/venv"

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY CMakeLists.txt ./
COPY csrc/ ./csrc/
COPY extern/ ./extern/

RUN VIRTUAL_ENV=/opt/venv uv pip install --no-deps .


FROM python:3.12-slim AS prod

RUN apt-get update && apt-get install -y --no-install-recommends \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

RUN pip uninstall -y pip setuptools wheel

RUN useradd -m -s /bin/bash appuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY assets/ ./assets/
COPY src/integration_app ./integration_app
COPY main.py ./

RUN mkdir -p /app/output && chown -R appuser:appuser /app/output

USER appuser

ENTRYPOINT ["python"]
CMD ["main.py"]