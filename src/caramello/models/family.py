from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

from caramello.models.familymember import FamilyMember


class Family(SQLModel, table=True):
    """Represents a family group in the system."""
    __tablename__ = "families"

    id: int = Field(primary_key=True, nullable=False)  # Internal primary key (numeric).
    uuid: UUID = Field(unique=True, nullable=False, default_factory=uuid4)  # Unique public identifier (UUID).
    name: str = Field(nullable=False, max_length=100)  # Name of the family.
    description: Optional[str] = Field(default=None, max_length=255)  # Optional description of the family.
    status: str = Field(nullable=False, max_length=20)  # Status of the family (e.g., active, archived).
    created_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)  # Timestamp of the record's creation.
    updated_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)  # Timestamp of the record's last update.
    members: List['User'] = Relationship(back_populates='families', link_model=FamilyMember)
    invitations: List['FamilyInvitation'] = Relationship(back_populates='family')
