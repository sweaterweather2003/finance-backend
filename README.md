# Finance Dashboard Backend

**Role-based Finance Records Management & Analytics API**

A complete FastAPI backend solution built for the **Finance Data Processing and Access Control Backend** assignment.

---

## Assignment Objective

The task was to build a backend for a finance dashboard system where different users interact with financial records based on their roles. The system should support:

- User and Role Management
- Financial Records Management (CRUD + filtering)
- Dashboard Summary APIs with aggregated analytics
- Access Control Logic based on roles
- Proper validation and error handling
- Data persistence

The scenario describes a system in which users have specific roles (Viewer, Analyst, Admin) that decide what they are allowed to do with financial data (income/expense entries) and dashboard insights.

---

## My Understanding of the Problem Statement

I understood the problem as building a secure backend for a finance dashboard where multiple users need to work with financial data, but each user type has different permissions.

Key points I took from the problem statement:
- Users have roles that control access (Viewer can only view dashboard, Analyst can view records, Admin has full control).
- Financial records must include amount, type (income/expense), category, date, and description.
- The backend must support full CRUD operations on records plus filtering by date, category, or type.
- A dedicated dashboard summary is required with aggregated data: total income, total expenses, net balance, category-wise totals, recent activity, and monthly trends.
- Access control must be enforced at the backend level.
- The system should handle validation, return clear errors, and persist data in a database.
- The focus is on clean architecture, maintainability, and logical business rules rather than just basic endpoints.

## What I’ve Done

I've built a complete, clean, and fully functional backend that meets the **requirements**:

### Implemented Features
- JWT Authentication with secure password hashing
- Role-based Access Control (Viewer, Analyst, Admin)
- User Management (create, list, get current user)
- Financial Records full CRUD + advanced filtering (date, category, type)
- Dashboard Summary API with totals, category breakdown, recent activity, and monthly trends
- Automatic admin user creation on startup (`admin` / `admin123`)
- Input validation using Pydantic
- Proper error handling and meaningful HTTP status codes
- Comprehensive Swagger documentation (`/docs`)
- CORS enabled for frontend integration
- Pagination support in record listing

---

## Tech Stack
- **Framework**: FastAPI 0.115
- **Database**: SQLite + SQLAlchemy 2.0 (ORM)
- **Validation**: Pydantic v2
- **Authentication**: JWT (python-jose) + Passlib (pbkdf2_sha256)

---

## Project Structure
finance-dashboard-backend/
├── main.py                 # App creation, lifespan, CORS, routers
├── database.py             # SQLAlchemy engine & session
├── models.py               # User & FinancialRecord models
├── schemas.py              # All Pydantic models & enums
├── crud.py                 # Pure database operations (repository pattern)
├── auth.py                 # JWT token & password utilities
├── dependencies.py         # Security & role-check dependencies
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── records.py
│   └── dashboard.py
├── requirements.txt
└── finance.db              # Auto-generated SQLite database



---

## Code Documentation

- **`main.py`**  
  Entry point of the application. Creates the FastAPI app, handles database table creation and default admin user seeding during startup (using lifespan), adds CORS middleware, and includes all routers.  
  *Why this design?* Central place for app initialization and one-time setup tasks.

- **`database.py`**  
  Configures SQLAlchemy engine, session factory, and the Base class for all models. Uses SQLite as the database.  
  *Why this design?* Keeps all database configuration in one clean, reusable file.

- **`models.py`**  
  Defines the SQLAlchemy ORM models: `User` and `FinancialRecord`.  
  *Why this design?* Clear separation between database tables and Python objects with automatic timestamps.

- **`schemas.py`**  
  Contains all Pydantic models (`UserCreate`, `FinancialRecordCreate`, `DashboardSummary`, etc.) and enums (`Role`, `RecordType`).  
  *Why this design?* Provides strict input/output validation and automatic OpenAPI/Swagger documentation.

- **`crud.py`**  
  Contains all database operations (create user, create/read/update/delete records, get dashboard summary, filtering, etc.).  
  *Why this design?* Pure data layer following the repository pattern — no HTTP or auth logic here. Makes the code highly testable and easy to maintain.

- **`auth.py`**  
  Handles password hashing, JWT token creation, and user authentication logic.  
  *Why this design?* Security-related code is completely isolated from the rest of the application.

- **`dependencies.py`**  
  Defines reusable FastAPI dependencies: `get_current_user`, `require_role`, and `get_analyst_or_admin`.  
  *Why this design?* Central place for all authorization checks. Keeps the code DRY and role-based access very clean.

- **`routers/auth.py`**  
  Contains only the `POST /auth/login` endpoint.  
  *Why this design?* Keeps authentication routes small and separate.

- **`routers/users.py`**  
  Handles user management endpoints (create user, list users, get current user `/me`).  
  *Why this design?* Protected by role-based dependencies.

- **`routers/records.py`**  
  Provides full CRUD operations and filtering for financial records.  
  *Why this design?* Different permissions are enforced per action (Admin vs Analyst).

- **`routers/dashboard.py`**  
  Contains the single endpoint `GET /dashboard/summary`.  
  *Why this design?* Dashboard-specific aggregated logic is kept in its own router.

**Overall Architecture**: Clean Architecture + Repository Pattern + Dependency Injection for maximum maintainability.



## Design Decisions

- **Clean Architecture & Separation of Concerns**  
  The project is structured with clear layers:  
  - Routers handle only HTTP requests and responses.  
  - Dependencies manage authentication and authorization.  
  - CRUD layer (`crud.py`) contains all business and database logic.  
  - Models and Schemas are purely definition files.  
  This separation makes the code highly readable, testable, and easy to maintain or extend.

- **Repository Pattern**  
  All database operations are centralized in `crud.py`. No raw SQLAlchemy queries are scattered across routers or other files. This follows the Repository Pattern, making data access consistent and future-proof (easy to switch from SQLite to PostgreSQL).

- **JWT-Based Authentication with Role Embedding**  
  Used JSON Web Tokens (JWT) for stateless authentication. The user’s `role` is embedded directly in the token payload. This eliminates extra database calls on every protected request and enables fast, efficient role-based authorization.

- **Reusable Dependency Injection for Authorization**  
  Created custom FastAPI dependencies (`get_current_user`, `require_role`, `get_analyst_or_admin`) in `dependencies.py`. This keeps all permission logic in one place (DRY principle) and makes role-based access control extremely clean and declarative.

- **Pydantic for Strict Validation**  
  All request and response models are defined using Pydantic v2. This provides automatic data validation, clear error messages, and excellent OpenAPI/Swagger documentation without extra effort.

- **Centralized Dashboard Analytics**  
  All aggregation logic (total income/expenses, category totals, monthly trends, recent activity) is implemented once in `crud.py` and reused by the dashboard router. This avoids code duplication and ensures consistent calculations.

- **Automatic Admin User Seeding**  
  Used FastAPI’s `lifespan` event to create the default admin user (`admin` / `admin123`) only on first startup. This provides an immediate working user without manual database setup.

- **Focus on Readability and Maintainability**  
  Chose clear naming conventions, detailed comments where needed, and kept functions small and single-responsibility. Prioritized production-ready practices even though this is an assignment project.

- **SQLite for Simplicity with Real ORM**  
  Used SQLite + SQLAlchemy 2.0 instead of in-memory storage. This demonstrates proper relational data modeling while keeping the setup simple and zero-config for reviewers.

These decisions were made to create a **professional-grade backend** that not only meets the functional requirements but also demonstrates strong backend engineering thinking, security awareness, and long-term maintainability.

---

## Commands to run

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd finance-dashboard-backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # On Windows
# source venv/bin/activate     # On Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn main:app --reload

Default Admin Credentials
Username: admin
Password: admin123
