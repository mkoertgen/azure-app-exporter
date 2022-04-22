import os

import uvicorn
from fastapi import FastAPI
from fastapi_health import health
from starlette_exporter import PrometheusMiddleware, handle_metrics

from logger import get_logger

APP_VERSION = os.getenv('APP_VERSION', 'unknown')
APP_NAME = os.getenv('APP_NAME', 'azure-sp-metrics-exporter')
APP_PORT = int(os.getenv('APP_PORT', '8000'))


async def is_healthy():
    return {"status": "UP"}


async def metrics_route(request):
    return handle_metrics(request)


app = FastAPI()

logger = get_logger(app, APP_NAME)

app.add_middleware(
    PrometheusMiddleware,
    group_paths=True,
    app_name=APP_NAME,
    prefix="http",
    skip_paths=['/health']
)
app.add_route("/metrics", metrics_route)
app.add_api_route("/health", health([is_healthy]))

logger.info(f"Starting {APP_NAME} (version={APP_VERSION}, port={APP_PORT})...")


@app.on_event("shutdown")
async def shutdown():
    logger.info(f"Shutting down {APP_NAME}...")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
