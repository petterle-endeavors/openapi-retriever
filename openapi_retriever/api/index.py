"""Define the main entry point for the API."""
from fastapi import FastAPI
from mangum import Mangum

from openapi_retriever.api.routers.health.routes import ROUTER as health_router


APP = FastAPI(
    title="OpenAPI Retriever",
    description="API that allows search and retrieval of OpenAPI specifications.",
    version="0.0.0",
)

APP.include_router(health_router, prefix="/health", tags=["health"])


handler = Mangum(APP)

