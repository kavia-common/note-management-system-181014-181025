"""
API routes for Notes.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import NoteCreate, NoteUpdate, NoteOut
from app.repositories.notes_repo import repo, to_note_out

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post(
    "",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note with a title and content. Returns the created note.",
    responses={
        201: {"description": "Note created successfully"},
        422: {"description": "Validation error"},
    },
)
def create_note(payload: NoteCreate) -> NoteOut:
    """
    Create a new note.

    Parameters:
    - payload: NoteCreate - The note data to create.

    Returns:
    - NoteOut: The created note with id and timestamps.
    """
    entity = repo.create_note(payload)
    return to_note_out(entity)


@router.get(
    "",
    response_model=List[NoteOut],
    summary="List notes",
    description="Retrieve all notes currently stored.",
)
def list_notes() -> List[NoteOut]:
    """
    List all notes.

    Returns:
    - List[NoteOut]: All notes in storage.
    """
    return [to_note_out(e) for e in repo.list_notes()]


@router.get(
    "/{note_id}",
    response_model=NoteOut,
    summary="Get note by ID",
    description="Retrieve a single note by its UUID.",
    responses={404: {"description": "Note not found"}},
)
def get_note(note_id: UUID) -> NoteOut:
    """
    Get a note by its ID.

    Parameters:
    - note_id: UUID - The unique identifier of the note.

    Returns:
    - NoteOut: The requested note.

    Raises:
    - HTTPException 404 if not found.
    """
    entity = repo.get_note(note_id)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return to_note_out(entity)


@router.put(
    "/{note_id}",
    response_model=NoteOut,
    summary="Update a note",
    description="Update an existing note's title and/or content.",
    responses={404: {"description": "Note not found"}},
)
def update_note(note_id: UUID, payload: NoteUpdate) -> NoteOut:
    """
    Update a note by its ID.

    Parameters:
    - note_id: UUID - The note ID.
    - payload: NoteUpdate - Fields to update.

    Returns:
    - NoteOut: The updated note.

    Raises:
    - HTTPException 404 if not found.
    - HTTPException 400 if payload has no updatable fields.
    """
    if payload.title is None and payload.content is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    entity = repo.update_note(note_id, payload)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return to_note_out(entity)


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its UUID.",
    responses={204: {"description": "Note deleted"}, 404: {"description": "Note not found"}},
)
def delete_note(note_id: UUID) -> None:
    """
    Delete a note by its ID.

    Parameters:
    - note_id: UUID - The note ID.

    Returns:
    - None (204 No Content)

    Raises:
    - HTTPException 404 if not found.
    """
    deleted = repo.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None
