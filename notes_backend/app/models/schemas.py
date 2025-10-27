"""
Pydantic schemas for the Notes API.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, constr


NoteTitle = constr(strip_whitespace=True, min_length=1, max_length=200)
NoteContent = constr(strip_whitespace=True, min_length=1, max_length=10_000)


class NoteBase(BaseModel):
    """Base fields shared across Note representations."""
    title: NoteTitle = Field(..., description="Title of the note")
    content: NoteContent = Field(..., description="Content/body of the note")


class NoteCreate(NoteBase):
    """Payload for creating a new note."""
    pass


class NoteUpdate(BaseModel):
    """Payload for updating an existing note; all fields optional."""
    title: Optional[NoteTitle] = Field(None, description="Updated title of the note")
    content: Optional[NoteContent] = Field(None, description="Updated content of the note")


class NoteOut(NoteBase):
    """Representation of a note returned by the API."""
    id: UUID = Field(..., description="Unique identifier of the note")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")

    class Config:
        from_attributes = True  # Enables compatibility with ORM-like objects
