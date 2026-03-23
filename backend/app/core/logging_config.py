"""Centralized logging configuration using loguru."""

import sys
import json
import logging
from contextvars import ContextVar
from typing import Optional
from datetime import datetime

from loguru import logger

# Context variable for trace ID
trace_id_var: ContextVar[str] = ContextVar("trace_id", default="-")


def get_trace_id() -> str:
    """Get current trace ID from context."""
    return trace_id_var.get()


def set_trace_id(trace_id: str) -> None:
    """Set trace ID in context."""
    trace_id_var.set(trace_id)


def json_formatter(record):
    """Custom JSON formatter for log records."""
    log_entry = {
        "timestamp": datetime.fromtimestamp(record["time"].timestamp()).isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "logger": record["name"],
        "function": record["function"],
        "line": record["line"],
        "file": record["file"].name,
        "trace_id": record["extra"].get("trace_id", get_trace_id()),
    }

    # Add exception info if present
    if record["exception"]:
        log_entry["exception"] = {
            "type": str(record["exception"].type),
            "value": str(record["exception"].value),
            "traceback": str(record["exception"].traceback),
        }

    return json.dumps(log_entry) + "\n"


def configure_logging():
    """Configure loguru with JSON format including trace ID."""
    # Remove default handler
    logger.remove()

    # Determine if we should use JSON format (based on environment variable)
    import os
    use_json_format = os.getenv("LOG_FORMAT", "text").lower() == "json"

    if use_json_format:
        # Add stdout handler with JSON format
        logger.add(
            sys.stdout,
            level="INFO",
            format=json_formatter,
            serialize=False,
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )
    else:
        # Add stdout handler with text format (including trace ID)
        logger.add(
            sys.stdout,
            level="INFO",
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[trace_id]: <12}</cyan> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

    # Patch the default logger to include trace_id in extra
    logger.patch(lambda record: record["extra"].update(trace_id=get_trace_id()))

    return logger


def intercept_standard_logging():
    """Redirect standard library logging to loguru."""
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding loguru level
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find the caller's frame
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Replace all standard logger handlers
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    for name in logging.root.manager.loggerDict:
        logging.getLogger(name).handlers = [InterceptHandler()]
        logging.getLogger(name).propagate = False


# Configure on import
configure_logging()
