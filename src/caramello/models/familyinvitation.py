from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr


class FamilyInvitation(SQLModel, table=True):
    """Manages the invitation flow for families."""
    __tablename__ = "family_invitations"

    id: int = Field(primary_key=True, nullable=False)  # Internal primary key (numeric).
    uuid: UUID = Field(unique=True, nullable=False, default_factory=uuid4)  # Unique public identifier (UUID).
    family_id: int = Field(nullable=False, foreign_key='families.id')  # ID of the family to which the invitation was sent.
    inviter_id: int = Field(nullable=False, foreign_key='users.id')  # ID of the user who sent the invitation.
    invitee_email: EmailStr = Field(nullable=False)  # Email of the invited user.
    status: str = Field(nullable=False, max_length=20)  # Status of the invitation (pending, accepted, declined).
    created_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)  # Timestamp of the invitation's creation.
    expires_at: datetime = Field(nullable=False)  # Timestamp of the invitation's expiration.
    family: 'Family' = Relationship(back_populates='invitations')
    inviter: 'User' = Relationship(back_populates='sent_invitations')
