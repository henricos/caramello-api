from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from datetime import datetime
from caramello.database.session import get_session
from caramello.models.family import Family

router = APIRouter(prefix="/family", tags=["Family"])

@router.post("/", response_model=Family)
def create_family(family: Family, session: Session = Depends(get_session)):
    session.add(family)
    session.commit()
    session.refresh(family)
    return family

@router.get("/", response_model=List[Family])
def read_familys(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    return session.exec(select(Family).offset(offset).limit(limit)).all()

@router.get("/{id}", response_model=Family)
def read_family(id: int, session: Session = Depends(get_session)):
    family = session.get(Family, id)
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return family
