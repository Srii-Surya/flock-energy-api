# Flock Energy Meter API

A read-only REST API built with FastAPI that retrieves meter information from the Urja Meter Ops portal.

## Features

- Read-only meter search endpoint
- Query and page parameters
- Pydantic response validation
- Upstream error handling
- Interactive Swagger documentation
- Automated API tests

## Tech Stack

- Python
- FastAPI
- HTTPX
- Pydantic
- Pytest

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Set `URJA_PORTAL_SESSION_COOKIE` in `.env` to a valid portal session cookie, if you are authorized to access the portal. Never commit `.env` or share your session cookie.

### 4. Run the API

```powershell
python -m uvicorn app.main:app --reload
```

Open:
- API root: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## Endpoint

`GET /api/v1/meters`

Query parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | empty | Meter search query |
| `page` | integer | 1 | Page number; must be at least 1 |

Example:

```http
GET /api/v1/meters?q=&page=1
```

The endpoint forwards the search to the upstream portal and returns the validated `data` list.

## Error handling

- `422`: Invalid query parameters
- `502`: Upstream portal unavailable, authentication failure, or invalid upstream response

## Tests

Run:

```powershell
python -m pytest -v
```

Tests use a mocked portal response and do not require a live session.

## Limitations

- A valid portal session is required for live meter requests.
- The API is read-only and does not modify portal data.
- Portal behavior beyond the observed search response has not been assumed.
