FROM python:3.11-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app


FROM base AS build-stage

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip wheel \
    && python -m pip wheel --no-cache-dir --wheel-dir /wheels \
    -r /app/requirements.txt


FROM base AS runtime-deps-stage

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build-stage /wheels /wheels
COPY --from=build-stage /app/requirements.txt /app/requirements.txt

RUN python -m pip install --no-index /wheels/* \
    && rm -rf /wheels /app/requirements.txt


FROM runtime-deps-stage AS run-stage

RUN addgroup --gid 10001 --system python && \
    adduser --no-create-home --shell /bin/false \
    --disabled-password --uid 10001 --system --group python

COPY --chown=python:python ./src/ /app/

USER python

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
