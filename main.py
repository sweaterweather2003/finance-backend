from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
from models import User
from auth import get_password_hash
import crud

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Seed default admin user (only once)
    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.role == "ADMIN").first()
        if not existing_admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                role="ADMIN",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("✅ Admin user created → username: admin | password: admin123")
    finally:
        db.close()
    yield

app = FastAPI(
    title="Finance Dashboard Backend",
    description="Role-based finance records + dashboard API (Assignment Solution)",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from routers import auth, users, records, dashboard

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(records.router, prefix="/records", tags=["records"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

@app.get("/")
def root():
    return RedirectResponse(url="/docs")