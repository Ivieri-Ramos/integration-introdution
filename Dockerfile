FROM python:3.14-slim AS builder

# TODO: Adicionar as bibliotecas de compilação de C++ quando tiver o código fonte

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT="/opt/venv"

COPY pyproject.toml uv.lock ./

RUN --mount=from=ghcr.io/astral-sh/uv:latest,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    /bin/uv sync --frozen --no-install-project

COPY csrc/ ./csrc/


FROM python:3.14-slim AS prod

RUN useradd -m -s /bin/bash appuser

RUN pip uninstall -y pip setuptools wheel

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY src/ ./src/
COPY main.py ./

USER appuser

ENTRYPOINT ["python"]
CMD ["main.py"]