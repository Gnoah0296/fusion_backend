from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from utils.db import get_db
from repositories.user_repository import UserRepository
from services.token import SECRET_KEY, ALGORITHM

oauth2_scheme = HTTPBearer()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    token = token.credentials  # Lấy đúng access token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    repo = UserRepository()
    user = repo.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
