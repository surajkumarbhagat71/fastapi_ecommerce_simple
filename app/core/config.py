import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123456@localhost:5432/fastapi_ecommerce"
)
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
