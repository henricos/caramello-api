from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

from caramello.models.familymember import FamilyMember


class User(SQLModel, table=True):
    """Represents a system user."""
    __tablename__ = "users"

    id: int = Field(primary_key=True, nullable=False)  # Internal primary key (numeric).
    uuid: UUID = Field(unique=True, nullable=False, default_factory=uuid4)  # Unique public identifier (UUID).
    full_name: str = Field(nullable=False, max_length=100)  # User's full name.
    email: EmailStr = Field(unique=True, nullable=False)  # Unique email address, used for login.
    phone_number: Optional[str] = Field(default=None, max_length=20)  # Phone number (E.164 format recommended).
    hashed_password: Optional[str] = Field(default=None)  # Hashed password (null for users via OAuth).
    google_id: Optional[str] = Field(unique=True, default=None)  # User's unique Google ID (for OAuth).
    avatar_url: Optional[str] = Field(default=None)  # URL of the user's profile picture.
    is_active: bool = Field(nullable=False)  # Indicates if the user is active in the system.
    created_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)  # Timestamp of the record's creation.
    updated_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)  # Timestamp of the record's last update.
    families: List['Family'] = Relationship(back_populates='members', link_model=FamilyMember)
    sent_invitations: List['FamilyInvitation'] = Relationship(back_populates='inviter')
