# imports
# built-in
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# user-defined


""" Receipt schema """

# base schema
class ReceiptBase(BaseModel):
    business_name: str = Field(..., example = "Shoprite Supermarket")
    date: str = Field(..., example = "28/09/2026")
    category: str = Field(..., example = "Food & Groceries")
    amount: float = Field(
        ..., gt = 0, description = "Amount must be greater than 0!", example = 12905 
    )
    vat: float = Field(default = 0.0, ge = 0.0, description = "VAT cannot be a negative number!", example = 800)
    payment_method: str = Field(..., example = "Card")
    # created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# schema for creating a receipt (data required from the user)
class ReceiptCreate (ReceiptBase):
    pass

# schema for returning a receipt (data sent back to the user)
class ReceiptResponse (ReceiptBase):
    id: str
    created_at: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    class Config:
        # allows pydantic to directly read data from database ORM models
        from_attributes = True

