# Simple FastAPI E-Commerce

Beginner-friendly FastAPI + SQLAlchemy ORM + PostgreSQL + Alembic project.

Features:
- Category
- Product
- User signup/login
- JWT authentication
- Login required for cart and order
- Cart stock check
- Order total calculation
- Stock reduction
- Alembic migrations

Setup:
1. Create PostgreSQL database `fastapi_ecommerce`.
2. Update `.env` if needed.
3. `pip install -r requirements.txt`
4. `alembic revision --autogenerate -m "initial ecommerce tables"`
5. `alembic upgrade head`
6. `uvicorn app.main:app --reload`
7. Open http://127.0.0.1:8000/docs

Flow:
Category -> Product -> Signup -> Login -> Authorize -> Cart -> Order

Note: Passwords are plain text only to keep this learning project simple. Do not use this authentication approach in a real production application; use password hashing and stronger validation.



#-------------------- command -------------------------

# Environment
python -m venv venv
venv\Scripts\activate

# Install
pip install -r requirements.txt

# Server
uvicorn app.main:app --reload

# Alembic
alembic init alembic
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
alembic current
alembic history
alembic downgrade -1

# Git
git status
git add .
git commit -m "message"
git push