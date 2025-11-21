from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr


class FamilyMember(SQLModel, table=True):
    """Association table connecting Users and Families, defining the role of each member."""
    __tablename__ = "family_members"

    user_id: int = Field(primary_key=True, nullable=False, foreign_key='users.id')  # Foreign key for the users table.
    family_id: int = Field(primary_key=True, nullable=False, foreign_key='families.id')  # Foreign key for the families table.
    role: str = Field(nullable=False, max_length=20)  # User's role in the family (e.g., admin, member).
    joined_at: datetime = Field(nullable=False, default_factory=datetime.utcnow)  # Timestamp of when the user joined the family.
    user: 'User' = Relationship(back_populates='families')
    family: 'Family' = Relationship(back_populates='members')
