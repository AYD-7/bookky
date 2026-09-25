from app.core.config import settings
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# configure CORS so React (Vite) can query backend without browser blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# root route
@app.get("/", tags="Root Route")
def root_path():
    """Root"""
    return {
        "status_code": status.HTTP_200_OK,
        "success": True,
        "message": f"Welcome to {settings.PROJECT_NAME}. Visit {settings.BACKEND_URL}docs for API documentation."

    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """Simple status check to verify server health."""
    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }