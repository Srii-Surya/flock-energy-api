from fastapi import FastAPI, HTTPException, Query

from app.portal_client import PortalClient, PortalClientError
from app.schemas import MeterSearchResponse

app = FastAPI(
    title="Flock Energy Meter API",
    description=(
        "A read-only API providing structured meter information "
        "from Urja Meter Ops."
    ),
    version="1.0.0",
)

portal = PortalClient()


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Flock Energy Meter API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.get(
    "/api/v1/meters",
    response_model=MeterSearchResponse,
    tags=["Meters"],
)
def list_meters(
    q: str = Query(default="", max_length=100),
    page: int = Query(default=1, ge=1),
):
    try:
        return portal.search_meters(query=q, page=page)
    except PortalClientError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc
