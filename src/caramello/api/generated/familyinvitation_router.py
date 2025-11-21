from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime
from caramello.database.session import get_session
from caramello.models.familyinvitation import FamilyInvitation

router = APIRouter(prefix="/family_invitations", tags=["FamilyInvitation"])

@router.post("/", response_model=FamilyInvitation)
def create_familyinvitation(familyinvitation: FamilyInvitation, session: Session = Depends(get_session)):
    session.add(familyinvitation)
    session.commit()
    session.refresh(familyinvitation)
    return familyinvitation

@router.get("/", response_model=List[FamilyInvitation])
def read_familyinvitations(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    return session.exec(select(FamilyInvitation).offset(offset).limit(limit)).all()

@router.get("/{id}", response_model=FamilyInvitation)
def read_familyinvitation(id: int, session: Session = Depends(get_session)):
    familyinvitation = session.get(FamilyInvitation, id)
    if not familyinvitation:
        raise HTTPException(status_code=404, detail="FamilyInvitation not found")
    return familyinvitation
