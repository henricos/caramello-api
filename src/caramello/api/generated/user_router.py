from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime
from caramello.database.session import get_session
from caramello.models.user import User

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/", response_model=List[User])
def read_users(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    return session.exec(select(User).offset(offset).limit(limit)).all()

@router.get("/{id}", response_model=User)
def read_user(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
