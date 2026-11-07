from typing import List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str
    quantity: float = 1
    unit_price: float
    total: float


class Invoice(BaseModel):
    invoice_number: str = Field(min_length=1)
    invoice_date: str = Field(description="YYYY-MM-DD")
    vendor_name: str = Field(min_length=1)
    customer_name: Optional[str] = None
    line_items: List[LineItem]
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total_amount: float
    currency: str = "INR"


class Education(BaseModel):
    institution: str
    degree: Optional[str] = None
    year: Optional[str] = None


class Resume(BaseModel):
    full_name: str = Field(min_length=1)
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str]
    education: List[Education]
    experience_summary: Optional[str] = None
    total_experience_years: Optional[float] = None


SCHEMAS = {"invoice": Invoice, "resume": Resume}