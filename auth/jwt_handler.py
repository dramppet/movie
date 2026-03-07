from datetime import datetime, timedelta, timezone
from jose import jwt
import os

TOKEN_EXP_TIME = 60
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_jwt(username: str, role_id: int) -> str: 
    payload = {
        "sub": username,
        "role_id": role_id, 
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXP_TIME)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)