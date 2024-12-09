"""
Healthcheck endpoint
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/healthcheck", include_in_schema=True)
async def healthcheck():
    """
    Perform a health check to determine if the service is running correctly.

    This function is an asynchronous endpoint that serves as a health check
    for the application. When invoked, it returns a JSON response with the
    status of the service, allowing services or monitoring tools to verify
    that the application is operational.

    Returns:
        JSONResponse: A JSON response containing the health status of the application.
    """
    return JSONResponse(content={"status": "healthy"})
