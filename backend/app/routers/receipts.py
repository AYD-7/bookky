from datetime import datetime
from typing import List
from app.schemas.receipts import ReceiptCreate, ReceiptResponse
from fastapi import APIRouter, HTTPException, status

# APIRouter acts like a mini FastAPI app for a specific feature
router = APIRouter(
    prefix="/receipts",
    tags=["Receipts"],  # Groups endpoints nicely in /docs
)

# Temporary in-memory list to act as our database for now
fake_receipts_db = []


@router.post(
    "/", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED
)
def create_receipt(receipt_in: ReceiptCreate):
    """Create a new receipt."""
    new_id = len(fake_receipts_db) + 1
    new_receipt = {
        "id": new_id,
        "created_at": datetime.now(),
        **receipt_in.model_dump(),
    }
    fake_receipts_db.append(new_receipt)
    return new_receipt


@router.get("/", response_model=List[ReceiptResponse])
def get_all_receipts():
    """Retrieve all receipts."""
    
    if (len(fake_receipts_db) < 0):
        raise HTTPException (
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No Receipts found"
        )

    return fake_receipts_db


@router.get("/{receipt_id}", response_model=ReceiptResponse)
def get_receipt(receipt_id: int):
    """Retrieve a single receipt by ID."""
    for receipt in fake_receipts_db:
        if receipt["id"] == receipt_id:
            return receipt

    # throw a proper HTTP 404 error if not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Receipt with ID {receipt_id} not found",
    )