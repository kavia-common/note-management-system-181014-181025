# This module previously hosted a minimal FastAPI app.
# The application has been restructured under the `app/` package with
# a full Notes CRUD implementation.
#
# The actual ASGI app entrypoint is now `app.main:app`.
# Keeping this file to avoid import errors if any tooling references it.

from app.main import app as app  # re-export the main app

__all__ = ["app"]

# No-op reference to ensure linters recognize usage in this file context.
_ = app
