from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --- USER SCHEMAS ---
class UserCreate(BaseModel):
    """Data required when someone signs up."""
    email: EmailStr
    password: str = Field(min_length = 6, max_length = 72, description="Minimum 6 characters long")
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseModel):
    """Safe user data returned back to the user (never return passwords!)."""
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """The JSON payload sent back after successful login."""
    access_token: str
    token_type: str = "bearer"


# --- RECEIPT SCHEMAS ---
class ReceiptBase(BaseModel):
    business_name: str
    amount: float = Field(gt=0)
    vat: float = Field(default=0.0, ge=0)
    category: str
    payment_method: str = "Card"


class ReceiptCreate(ReceiptBase):
    """Data required to create a new receipt."""
    pass


class ReceiptUpdate(BaseModel):
    """Fields that can be updated optionally on a receipt."""
    business_name: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0)
    vat: Optional[float] = Field(default=None, ge=0)
    category: Optional[str] = None
    payment_method: Optional[str] = None


class ReceiptResponse(ReceiptBase):
    """Full receipt payload sent back to the frontend."""
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)