from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Receipt, User
from app.routers.deps import get_current_user
from app.schemas.schemas import ReceiptCreate, ReceiptResponse, ReceiptUpdate

router = APIRouter(prefix="/receipts", tags=["Receipts"])


@router.post("/", response_model = ReceiptResponse, status_code = status.HTTP_201_CREATED)
def create_receipt(
    receipt_in: ReceiptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Creates a new receipt owned by the currently logged-in user."""
    db_receipt = Receipt(**receipt_in.model_dump(), user_id = current_user.id)
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt


@router.get("/", response_model=List[ReceiptResponse])
def get_user_receipts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetches all receipts that belong ONLY to the logged-in user."""
    return db.query(Receipt).filter(Receipt.user_id == current_user.id).all()


@router.get("/{receipt_id}", response_model=ReceiptResponse)
def get_single_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Gets a single receipt by ID (ensuring it belongs to the current user)."""
    receipt = (
        db.query(Receipt)
        .filter(Receipt.id == receipt_id, Receipt.user_id == current_user.id)
        .first()
    )
    if not receipt:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Receipt not found or you don't have access to it",
        )
    return receipt


@router.put("/{receipt_id}", response_model=ReceiptResponse)
def update_receipt(
    receipt_id: int,
    receipt_in: ReceiptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update receipt information."""
    receipt = (
        db.query(Receipt)
        .filter(Receipt.id == receipt_id, Receipt.user_id == current_user.id)
        .first()
    )
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    # Update only the fields provided in the request
    update_data = receipt_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(receipt, field, value)

    db.commit()
    db.refresh(receipt)
    return receipt


@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a receipt owned by the user."""
    receipt = (
        db.query(Receipt)
        .filter(Receipt.id == receipt_id, Receipt.user_id == current_user.id)
        .first()
    )
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    db.delete(receipt)
    db.commit()
    return None