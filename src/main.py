import uvicorn
from fastapi import FastAPI

from api import add_api
from core.config import settings
from observability import add_observability


def create_app() -> FastAPI:
    the_app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_BASE}/openapi.json")
    add_observability(the_app)
    add_api(the_app)
    return the_app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
