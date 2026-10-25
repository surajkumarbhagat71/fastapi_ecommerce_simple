from datetime import datetime, timedelta
from jose import jwt
from app.core.config import SECRET_KEY

def create_token(user_id: int):
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=2)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
