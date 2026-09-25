from app.core.config import settings
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime

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
@app.get("/", tags=["Root Route"])
def root():
    """Root"""
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": f"Welcome to {settings.PROJECT_NAME}. Visit /docs for API documentation."

    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """Simple status check to verify server health."""
    return {
        "success": True,
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }

# receipts routes

# GET requests
@app.get("/receipts", tags=["Get All Receipts"])
def get_all_receipts ():
    """Gets all receipts for a user"""

    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "Receipts fetched successfully",
        "data": {
            "data": "receipts"
        }
    }


@app.get("/receipts/{receipt_id}", tags=["Get A Receipt By Id"])
def get_receipt_by_id (receipt_id: int):    # pydantic implicitly turns the receipt's id to an integer
    """Gets a single receipt for a user"""
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "Receipt fetched successfully",
        "data": {
            "id": receipt_id,
            "data": "receipt",
        }
    }

@app.get("/search", tags=["Search Receipts"])
def search_receipt (category: str, limit: int = 10): 
    """Searches for receipt in a category"""
    return {
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "Search is successful",
        "search_category": category,
        "limit": limit,
    }


# receipt schema
class ReceiptCreate(BaseModel):
    business_name: str
    date: str
    category: str
    amount: float = Field(
        gt = 0, description = "Amount must be greater than 0!"
    )
    vat: float = 0.00
    payment_method: str 
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# POST requests
@app.post("/receipts", tags=["Create A Receipt"])
def create_receipt (receipt: ReceiptCreate):
    total_amount: float = receipt.amount + receipt.vat
    return {
        "success": True,
        "status_code": status.HTTP_201_CREATED,
        "message": "Receipt created successfully",
        "received_data": receipt.model_dump(),
        "calculated_total": total_amount
    }