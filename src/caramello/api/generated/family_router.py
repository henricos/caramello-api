from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from caramello.database.session import get_session
from caramello.models.family import Family, FamilyRead, FamilyCreate, FamilyUpdate

router = APIRouter(prefix="/family", tags=["Family"])

@router.post("/", response_model=FamilyRead)
def create_family(family_in: FamilyCreate, session: Session = Depends(get_session)):
    db_obj = Family.model_validate(family_in)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.get("/", response_model=List[FamilyRead])
def read_familys(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    return session.exec(select(Family).offset(offset).limit(limit)).all()

@router.get("/{uuid}", response_model=FamilyRead)
def read_family(uuid: UUID, session: Session = Depends(get_session)):
    statement = select(Family).where(Family.uuid == uuid)
    family = session.exec(statement).first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return family

@router.patch("/{uuid}", response_model=FamilyRead)
def update_family(uuid: UUID, family_in: FamilyUpdate, session: Session = Depends(get_session)):
    statement = select(Family).where(Family.uuid == uuid)
    db_obj = session.exec(statement).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Family not found")
        
    hero_data = family_in.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_obj, key, value)
        
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.delete("/{uuid}")
def delete_family(uuid: UUID, session: Session = Depends(get_session)):
    statement = select(Family).where(Family.uuid == uuid)
    db_obj = session.exec(statement).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Family not found")
        
    session.delete(db_obj)
    session.commit()
    return {"ok": True}
