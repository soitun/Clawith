"""
Monitoring and metrics middleware for Clawith backend
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from app.config import get_settings
import time
import re

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'http_active_connections',
    'Active HTTP connections'
)

# Create regex to clean dynamic routes (e.g., /api/users/{id} instead of /api/users/123)
def clean_path(path: str) -> str:
    # Replace UUIDs
    path = re.sub(r'/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', '/{id}', path)
    # Replace numeric IDs
    path = re.sub(r'/\d+', '/{id}', path)
    return path


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Increment active connections
        ACTIVE_CONNECTIONS.inc()

        method = request.method
        path = clean_path(request.url.path)

        start_time = time.time()

        try:
            response = await call_next(request)
        finally:
            # Decrement active connections
            ACTIVE_CONNECTIONS.dec()

            # Record metrics
            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status_code=response.status_code
            ).inc()

            duration = time.time() - start_time
            REQUEST_LATENCY.labels(
                method=method,
                endpoint=path
            ).observe(duration)

        return response


def metrics_endpoint():
    """Metrics endpoint for Prometheus scraping"""
    return Response(content=generate_latest(), media_type='text/plain')