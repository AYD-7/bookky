from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, engine
import app.models.models  # Registers database tables with SQLAlchemy
from app.routers import auth, receipts

# Build all tables inside test.db automatically when application starts
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS enables React / mobile frontends to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers under /api/v1
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}")
app.include_router(receipts.router, prefix=f"{settings.API_V1_STR}")


@app.get("/")
def home():
    return {"message": "Welcome to Bookky API!", "docs": "/docs"}

@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }