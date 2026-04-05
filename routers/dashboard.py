from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import DashboardSummary, FinancialRecordOut
from models import User
from dependencies import get_current_user

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = crud.get_dashboard_summary(db)
    return DashboardSummary(
        total_income=data["total_income"],
        total_expenses=data["total_expenses"],
        net_balance=data["net_balance"],
        category_totals=data["category_totals"],
        recent_activity=[FinancialRecordOut.model_validate(r) for r in data["recent_activity"]],
        monthly_trends=data["monthly_trends"]
    )