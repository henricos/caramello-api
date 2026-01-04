from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from caramello.database.session import get_session
from caramello.models.familyinvitation import FamilyInvitation, FamilyInvitationRead, FamilyInvitationCreate, FamilyInvitationUpdate

router = APIRouter(prefix="/family_invitation", tags=["FamilyInvitation"])

@router.post("/", response_model=FamilyInvitationRead)
def create_familyinvitation(familyinvitation_in: FamilyInvitationCreate, session: Session = Depends(get_session)):
    db_obj = FamilyInvitation.model_validate(familyinvitation_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.get("/", response_model=List[FamilyInvitationRead])
def read_familyinvitations(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return session.exec(select(FamilyInvitation).offset(offset).limit(limit)).all()

@router.get("/{uuid}", response_model=FamilyInvitationRead)
def read_familyinvitation(uuid: UUID, session: Session = Depends(get_session)):
    statement = select(FamilyInvitation).where(FamilyInvitation.uuid == uuid)
    familyinvitation = session.exec(statement).first()
    if not familyinvitation:
        raise HTTPException(status_code=404, detail="FamilyInvitation not found")
    return familyinvitation

@router.patch("/{uuid}", response_model=FamilyInvitationRead)
def update_familyinvitation(uuid: UUID, familyinvitation_in: FamilyInvitationUpdate, session: Session = Depends(get_session)):
    statement = select(FamilyInvitation).where(FamilyInvitation.uuid == uuid)
    db_obj = session.exec(statement).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="FamilyInvitation not found")
        
    hero_data = familyinvitation_in.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_obj, key, value)
        
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.delete("/{uuid}")
def delete_familyinvitation(uuid: UUID, session: Session = Depends(get_session)):
    statement = select(FamilyInvitation).where(FamilyInvitation.uuid == uuid)
    db_obj = session.exec(statement).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="FamilyInvitation not found")
        
    session.delete(db_obj)
    session.commit()
    return {"ok": True}
