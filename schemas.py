from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

class RecordType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class Role(str, Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: Role
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class FinancialRecordCreate(BaseModel):
    amount: float = Field(..., gt=0)
    type: RecordType
    category: str
    date: date
    description: Optional[str] = None

class FinancialRecordOut(BaseModel):
    id: int
    amount: float
    type: RecordType
    category: str
    date: date
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class FinancialRecordFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category: Optional[str] = None
    type: Optional[RecordType] = None

class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    category_totals: dict
    recent_activity: List[FinancialRecordOut]
    monthly_trends: dict

class Login(BaseModel):
    username: str
    password: str