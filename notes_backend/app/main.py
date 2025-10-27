"""
FastAPI application entrypoint for the Notes API.

This service provides CRUD operations for notes.

Routes:
- GET /health: Health check endpoint returning {"status": "ok"}.
- POST /notes: Create a new note.
- GET /notes: List notes.
- GET /notes/{id}: Get a note by ID.
- PUT /notes/{id}: Update a note.
- DELETE /notes/{id}: Delete a note.

OpenAPI documentation is available at /docs and /openapi.json.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.routes import notes as notes_routes


def create_app() -> FastAPI:
    """Instantiate and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        openapi_tags=[
            {"name": "Health", "description": "Service health and status"},
            {"name": "Notes", "description": "CRUD operations for notes"},
        ],
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health endpoint
    @app.get(
        "/health",
        tags=["Health"],
        summary="Health check",
        description="Returns service status for health checks.",
    )
    # PUBLIC_INTERFACE
    def health() -> dict:
        """Health check endpoint."""
        return {"status": "ok"}

    # Register routes
    app.include_router(notes_routes.router)

    return app


# The ASGI application used by uvicorn
app = create_app()
