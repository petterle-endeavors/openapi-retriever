"""Define routes for health checks."""
from fastapi import APIRouter


ROUTER = APIRouter()


@ROUTER.get("/status")
def health():
    """Return a 200 response."""
    return {"status": "ok"}
