from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.logger import logger
from app.routes.home import router as home_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home_router)


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": "1.0.0",
    }


logger.info("Application started")