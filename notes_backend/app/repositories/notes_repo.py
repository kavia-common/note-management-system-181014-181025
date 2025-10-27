"""
In-memory repository for managing notes.
This layer abstracts storage operations so we can later switch to a real database.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from threading import RLock
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from app.models.schemas import NoteCreate, NoteUpdate, NoteOut


@dataclass
class NoteEntity:
    """Internal representation of a Note in the repository."""
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class NotesRepository:
    """Thread-safe in-memory notes repository with CRUD operations."""

    def __init__(self) -> None:
        self._store: Dict[UUID, NoteEntity] = {}
        self._lock = RLock()

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[NoteEntity]:
        """Return all notes in insertion order."""
        with self._lock:
            return list(self._store.values())

    # PUBLIC_INTERFACE
    def create_note(self, payload: NoteCreate) -> NoteEntity:
        """Create a note and persist it in memory."""
        now = datetime.now(timezone.utc)
        entity = NoteEntity(
            id=uuid4(),
            title=payload.title,
            content=payload.content,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._store[entity.id] = entity
        return entity

    # PUBLIC_INTERFACE
    def get_note(self, note_id: UUID) -> Optional[NoteEntity]:
        """Get a single note by its ID."""
        with self._lock:
            return self._store.get(note_id)

    # PUBLIC_INTERFACE
    def update_note(self, note_id: UUID, payload: NoteUpdate) -> Optional[NoteEntity]:
        """Update fields of a note if it exists."""
        with self._lock:
            entity = self._store.get(note_id)
            if not entity:
                return None
            updated = False
            if payload.title is not None:
                entity.title = payload.title
                updated = True
            if payload.content is not None:
                entity.content = payload.content
                updated = True
            if updated:
                entity.updated_at = datetime.now(timezone.utc)
            self._store[note_id] = entity
            return entity

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: UUID) -> bool:
        """Delete a note by ID. Returns True if it existed."""
        with self._lock:
            return self._store.pop(note_id, None) is not None


# Singleton repository instance used by the API layer for this simple app.
repo = NotesRepository()


# PUBLIC_INTERFACE
def to_note_out(entity: NoteEntity) -> NoteOut:
    """Transform a NoteEntity to the public NoteOut schema."""
    return NoteOut(
        id=entity.id,
        title=entity.title,
        content=entity.content,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
