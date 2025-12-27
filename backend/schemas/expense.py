from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExpenseBase(BaseModel):
    description: str
    amount: float
    category: Optional[str] = None
    payment_method: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    date: datetime
    ai_category: Optional[str] = None
    ai_confidence: Optional[float] = None
    
    class Config:
        from_attributes = True