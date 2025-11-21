from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime
from caramello.database.session import get_session
from caramello.models.familymember import FamilyMember

router = APIRouter(prefix="/family_members", tags=["FamilyMember"])

@router.post("/", response_model=FamilyMember)
def create_familymember(familymember: FamilyMember, session: Session = Depends(get_session)):
    session.add(familymember)
    session.commit()
    session.refresh(familymember)
    return familymember

@router.get("/", response_model=List[FamilyMember])
def read_familymembers(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    return session.exec(select(FamilyMember).offset(offset).limit(limit)).all()

@router.get("/{user_id}", response_model=FamilyMember)
def read_familymember(user_id: int, session: Session = Depends(get_session)):
    familymember = session.get(FamilyMember, user_id)
    if not familymember:
        raise HTTPException(status_code=404, detail="FamilyMember not found")
    return familymember
