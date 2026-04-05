from sqlalchemy.orm import Session
from sqlalchemy import func
from models import User, FinancialRecord
from schemas import UserCreate, FinancialRecordCreate, FinancialRecordFilter
from datetime import date

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Fixed: now accepts already-hashed password (breaks circular import)
def create_user(db: Session, user: UserCreate, hashed_password: str):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role.value,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_record(db: Session, record: FinancialRecordCreate):
    db_record = FinancialRecord(
        amount=record.amount,
        type=record.type.value,
        category=record.category,
        date=record.date,
        description=record.description
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_records(db: Session, filters: FinancialRecordFilter | None = None, skip: int = 0, limit: int = 100):
    query = db.query(FinancialRecord)
    if filters:
        if filters.start_date:
            query = query.filter(FinancialRecord.date >= filters.start_date)
        if filters.end_date:
            query = query.filter(FinancialRecord.date <= filters.end_date)
        if filters.category:
            query = query.filter(FinancialRecord.category == filters.category)
        if filters.type:
            query = query.filter(FinancialRecord.type == filters.type.value)
    return query.order_by(FinancialRecord.date.desc()).offset(skip).limit(limit).all()

def get_record(db: Session, record_id: int):
    return db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

def update_record(db: Session, record_id: int, record_data: FinancialRecordCreate):
    db_record = get_record(db, record_id)
    if db_record:
        db_record.amount = record_data.amount
        db_record.type = record_data.type.value
        db_record.category = record_data.category
        db_record.date = record_data.date
        db_record.description = record_data.description
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int):
    db_record = get_record(db, record_id)
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record

def get_dashboard_summary(db: Session):
    total_income = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == "income").scalar() or 0.0
    total_expenses = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == "expense").scalar() or 0.0

    category_totals = {}
    for cat, total in db.query(FinancialRecord.category, func.sum(FinancialRecord.amount)).group_by(FinancialRecord.category).all():
        category_totals[cat] = total or 0.0

    recent_activity = db.query(FinancialRecord).order_by(FinancialRecord.created_at.desc()).limit(10).all()

    monthly_trends = {}
    for month, total in db.query(
        func.strftime("%Y-%m", FinancialRecord.date).label("month"),
        func.sum(FinancialRecord.amount).label("total")
    ).group_by("month").order_by("month").all():
        monthly_trends[month] = total or 0.0

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": total_income - total_expenses,
        "category_totals": category_totals,
        "recent_activity": recent_activity,
        "monthly_trends": monthly_trends
    }