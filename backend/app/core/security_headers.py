"""
Security headers and security-related middleware
"""

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.security import SecurityMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware


def add_security_headers(app: FastAPI):
    """Add security headers to the application."""

    # Add security middleware
    app.add_middleware(
        SecurityMiddleware,
        # HSTS headers
        hsts_max_age=31536000,  # 1 year
        hsts_include_subdomains=True,
        hsts_preload=True,
        # Other security settings
        content_security_policy="default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' ws: wss:; frame-ancestors 'none'; object-src 'none'; base-uri 'self';",
        strict_transport_security="max-age=31536000; includeSubDomains; preload",
        referrer_policy="strict-origin-when-cross-origin",
    )

    return app