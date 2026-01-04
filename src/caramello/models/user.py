from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from caramello.models.familymember import FamilyMember

class User(SQLModel, table=True):
    """Represents a system user."""
    __tablename__ = "user"

    id: Optional['int'] = Field(primary_key=True, default=None)
    uuid: UUID = Field(unique=True, default_factory=uuid4, nullable=False)
    full_name: 'str' = Field(max_length=100, nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    phone_number: Optional['str'] = Field(max_length=20, default=None)
    hashed_password: Optional['str'] = Field(default=None)
    google_id: Optional['str'] = Field(unique=True, default=None)
    avatar_url: Optional['str'] = Field(default=None)
    is_active: 'bool' = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    families: list['Family'] = Relationship(back_populates='members', link_model=FamilyMember)
    sent_invitations: list['FamilyInvitation'] = Relationship(back_populates='inviter')

class UserRead(SQLModel):
    uuid: UUID
    full_name: 'str'
    email: EmailStr
    phone_number: Optional['str']
    google_id: Optional['str']
    avatar_url: Optional['str']
    is_active: 'bool'
    created_at: datetime
    updated_at: datetime

class UserCreate(SQLModel):
    full_name: 'str'
    email: EmailStr
    phone_number: Optional['str'] = None
    password: str
    google_id: Optional['str'] = None
    avatar_url: Optional['str'] = None
    is_active: Optional['bool'] = None

class UserUpdate(SQLModel):
    full_name: Optional['str'] = None
    email: Optional[EmailStr] = None
    phone_number: Optional['str'] = None
    password: Optional[str] = None
    google_id: Optional['str'] = None
    avatar_url: Optional['str'] = None
    is_active: Optional['bool'] = None

