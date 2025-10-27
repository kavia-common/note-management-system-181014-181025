# Notes Backend (FastAPI)

A simple Notes management API with CRUD operations.

## Run

If using uvicorn directly:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 3001 --reload
```

In the Kavia preview environment this service will be served on the preview port.

Docs: http://localhost:3001/docs  
OpenAPI JSON: http://localhost:3001/openapi.json

## Health

```bash
curl -s http://localhost:3001/health
# {"status":"ok"}
```

## CRUD Examples

Create:
```bash
curl -s -X POST http://localhost:3001/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"First Note","content":"Hello, world!"}'
```

List:
```bash
curl -s http://localhost:3001/notes
```

Get by ID:
```bash
NOTE_ID=<uuid-from-create>
curl -s http://localhost:3001/notes/$NOTE_ID
```

Update:
```bash
NOTE_ID=<uuid-from-create>
curl -s -X PUT http://localhost:3001/notes/$NOTE_ID \
  -H "Content-Type: application/json" \
  -d '{"content":"Updated content"}'
```

Delete:
```bash
NOTE_ID=<uuid-from-create>
curl -i -X DELETE http://localhost:3001/notes/$NOTE_ID
```

## Project Structure

```
notes_backend/
  app/
    __init__.py
    main.py
    core/
      config.py
    api/
      routes/
        notes.py
    models/
      schemas.py
    repositories/
      notes_repo.py
  .env.example
  requirements.txt
```

## Environment

Copy `.env.example` to `.env` and set variables as needed.

Supported:
- `APP_NAME`
- `APP_DESCRIPTION`
- `APP_VERSION`
- `CORS_ALLOWED_ORIGINS` (comma-separated, default "*")
