import json_logging
from fastapi import FastAPI
from fastapi_health import health
from starlette_exporter import PrometheusMiddleware, handle_metrics

from core.config import settings


def is_healthy():
    return {"status": "UP"}


def add_health(app: FastAPI):
    app.add_api_route("/health", health([is_healthy]))


def add_logging(app: FastAPI):
    enable_json = json_logging.ENABLE_JSON_LOGGING
    if not enable_json:
        return
    json_logging.init_fastapi(enable_json=True)
    json_logging.init_request_instrument(app)


def add_metrics(app: FastAPI):
    app.add_middleware(PrometheusMiddleware,
                       group_paths=True,
                       app_name=settings.PROJECT_NAME,
                       prefix="http",
                       skip_paths=['/health'])
    app.add_route("/metrics", handle_metrics)


def add_observability(app: FastAPI):
    add_health(app)
    add_logging(app)
    add_metrics(app)
