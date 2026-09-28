from app.core.config import settings
from app.routers import receipts  # Import our new router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the receipts router in our app
app.include_router(receipts.router, prefix=settings.API_V1_STR)


@app.get("/")
def home():
    return {
        "message": "Welcome to Bookky API!",
        "docs": "http://127.0.0.1:8000/docs",
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }