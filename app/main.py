from fastapi import FastAPI

from app.api.routes import health
from app.core.config import settings

app = FastAPI(title="AStock Agent System", version="0.1.0")

app.include_router(health.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.app_host, port=settings.app_port, reload=True)
