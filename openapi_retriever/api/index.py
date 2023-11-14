"""Define the main entry point for the API."""
from fastapi import FastAPI
from mangum import Mangum

from openapi_retriever.api.routers.admin.routes import ROUTER as health_router
from openapi_retriever.api.routers.openapi.routes import ROUTER as openapi_router
from openapi_retriever.api.settings import (
    Settings,
    RUNTIME_SETTINGS_ATTRIBUTE_NAME,
)


APP = FastAPI(
    title="OpenAPI Retriever",
    description="API that allows search and retrieval of OpenAPI specifications.",
    version="0.0.0",
)
setattr(APP.state, RUNTIME_SETTINGS_ATTRIBUTE_NAME, Settings())
APP.include_router(health_router, prefix="/admin", tags=["admin"])
APP.include_router(openapi_router, prefix="/openapi", tags=["openapi"])


handler = Mangum(APP)
