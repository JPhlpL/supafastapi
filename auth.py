# auth.py
from fastapi import status, HTTPException, Depends
from decouple import config
from supabase import create_client, Client
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Initialize Supabase client
supabase: Client = create_client(config("SUPERBASE_URL"), config("SUPERBASE_KEY"))

# JWT Settings
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model
class User(BaseModel):
    username: str
    password: str

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Authenticate user
def authenticate_user(username: str, password: str):
    user = supabase.table("users").select("*").eq("username", username).execute().get("data")[0]
    if not user or not pwd_context.verify(password, user["password"]):
        return False
    return user

# Create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Middleware for authentication
async def oauth2_scheme(token: str = Depends(config.oauth2_scheme)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user_id
