from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from caramello.database.session import get_session
from caramello.models.user import User, UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    db_obj = User.model_validate(user_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.get("/", response_model=List[UserRead])
def read_users(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return session.exec(select(User).offset(offset).limit(limit)).all()

@router.get("/{uuid}", response_model=UserRead)
def read_user(uuid: UUID, session: Session = Depends(get_session)):
    statement = select(User).where(User.uuid == uuid)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{uuid}", response_model=UserRead)
def update_user(uuid: UUID, user_in: UserUpdate, session: Session = Depends(get_session)):
    statement = select(User).where(User.uuid == uuid)
    db_obj = session.exec(statement).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
        
    hero_data = user_in.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_obj, key, value)
        
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.delete("/{uuid}")
def delete_user(uuid: UUID, session: Session = Depends(get_session)):
    statement = select(User).where(User.uuid == uuid)
    db_obj = session.exec(statement).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")
        
    session.delete(db_obj)
    session.commit()
    return {"ok": True}
