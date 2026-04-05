from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import FinancialRecordCreate, FinancialRecordOut, FinancialRecordFilter, RecordType, Role
from dependencies import require_role, get_analyst_or_admin
from models import User
from datetime import date
from typing import Optional

router = APIRouter()

@router.post("/", response_model=FinancialRecordOut)
def create_record(
    record: FinancialRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(Role.ADMIN))
):
    return crud.create_record(db, record)

@router.get("/", response_model=list[FinancialRecordOut])
def read_records(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    type: Optional[RecordType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_analyst_or_admin)
):
    filters = FinancialRecordFilter(
        start_date=start_date, end_date=end_date, category=category, type=type
    )
    return crud.get_records(db, filters, skip, limit)

@router.get("/{record_id}", response_model=FinancialRecordOut)
def read_record(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_analyst_or_admin)):
    record = crud.get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/{record_id}", response_model=FinancialRecordOut)
def update_record(
    record_id: int,
    record: FinancialRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(Role.ADMIN))
):
    updated = crud.update_record(db, record_id, record)
    if not updated:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated

@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(Role.ADMIN))
):
    deleted = crud.delete_record(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"message": "Record deleted"}