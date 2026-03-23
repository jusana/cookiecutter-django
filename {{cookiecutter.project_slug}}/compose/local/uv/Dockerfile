FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS python

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

# git requis pour les paquets git+https:// lors de uv add
RUN apt-get update && apt-get install --no-install-recommends -y git \
  && rm -rf /var/lib/apt/lists/*
