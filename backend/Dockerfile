# ─── Backend Dockerfile (Optimized) ─────────────────────
# Multi-stage: deps → production
FROM python:3.12-alpine AS deps

WORKDIR /app
RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev curl shadowsocks-libev

COPY pyproject.toml ./
ARG CLAWITH_PIP_INDEX_URL
ARG CLAWITH_PIP_TRUSTED_HOST
RUN if [ -n "$CLAWITH_PIP_INDEX_URL" ] && [ -n "$CLAWITH_PIP_TRUSTED_HOST" ]; then \
        pip install --no-cache-dir --index-url "$CLAWITH_PIP_INDEX_URL" --trusted-host "$CLAWITH_PIP_TRUSTED_HOST" .; \
    elif [ -n "$CLAWITH_PIP_INDEX_URL" ]; then \
        pip install --no-cache-dir --index-url "$CLAWITH_PIP_INDEX_URL" .; \
    else \
        pip install --no-cache-dir .; \
    fi

# ─── Production ─────────────────────────────────────────
FROM python:3.12-alpine AS production

WORKDIR /app

# Create non-root user
RUN apk add --no-cache libpq5 curl shadowsocks-libev dumb-init && \
    addgroup -g 1001 -S clawith && \
    adduser -S clawith -u 1001 -G clawith

# Copy installed packages from deps stage
COPY --from=deps --chown=clawith:clawith /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=deps --chown=clawith:clawith /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY --chown=clawith:clawith . .

# Create data directory and set permissions
RUN mkdir -p /data/agents && \
    chown -R clawith:clawith /app /data && \
    chmod +x /app/entrypoint.sh

USER clawith

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

EXPOSE 8000
# entrypoint.sh runs `alembic upgrade head` then `uvicorn`
ENTRYPOINT ["dumb-init", "/bin/bash", "/app/entrypoint.sh"]
