# Flock Energy Meter API

A read-only REST API built with FastAPI that provides structured meter information from the Urja Meter Ops portal.

## Features

- Retrieve meter records through a REST API.
- Support meter search using a query parameter.
- Support page-based requests.
- Validate responses using Pydantic schemas.
- Handle upstream HTTP, authentication, and response-format errors.
- Provide interactive API documentation using Swagger UI.
- Load portal configuration from environment variables.
- Include automated tests for API behavior.

## Technology Stack

- Python
- FastAPI
- HTTPX
- Pydantic
- Pytest
- Uvicorn

## Project Structure

```text
flock-energy-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── portal_client.py
│   └── schemas.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── PROTOCOL.md
├── README.md
└── openapi.json
```

## Prerequisites

- Python 3.11 or newer
- pip
- An authorized session for the upstream portal

## Setup

### 1. Clone the repository

```bash
git clone YOUR_PUBLIC_REPOSITORY_URL
cd flock-energy-api
```

Replace `YOUR_PUBLIC_REPOSITORY_URL` with the actual GitHub repository URL.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Install the dependencies used by the project:

```bash
python -m pip install fastapi "uvicorn[standard]" httpx pydantic-settings pytest
```

### 4. Configure environment variables

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configure the following variables in `.env`:

```dotenv
URJA_PORTAL_BASE_URL=https://urja-ops.flockenergy.tech
URJA_PORTAL_SESSION_COOKIE=
```

Set the session cookie locally using an authorized authentication session. Do not commit `.env` or share its contents.

**Authentication limitation:** The current implementation depends on a manually supplied session cookie. Session renewal and automated login are not implemented.

## Run the API

From the project root, run:

```bash
uvicorn app.main:app --reload
```

The local service will be available at:

- API root: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## API Endpoints

### Health check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### List or search meters

```http
GET /api/v1/meters?q=&page=1
```

Query parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | String | Empty string | Search query passed to the upstream portal |
| `page` | Integer | `1` | Page number; must be at least 1 |

Example request:

```http
GET http://127.0.0.1:8000/api/v1/meters?q=J100000&page=1
```

The returned meter fields include `meterId`, `serialNo`, `make`, `phaseType`, `installStatus`, and `dtCode` when provided by the upstream response.

The API currently models a top-level `data` array. Additional response fields are ignored by the Pydantic meter model.

### Error handling

- `422 Unprocessable Entity`: Invalid query parameters.
- `502 Bad Gateway`: Upstream portal request, authentication, or response processing failed.

## Run Automated Tests

Ensure pytest is installed in the active virtual environment:

```bash
python -m pip install pytest
```

Run the test suite:

```bash
python -m pytest -v
```

Tests use mocked upstream responses so they can run without relying on a live portal session.

## Portal Protocol Notes

See [PROTOCOL.md](PROTOCOL.md) for the observed upstream endpoint, authentication details, response structure, implementation notes, and known limitations.

## OpenAPI Specification

The FastAPI application generates its OpenAPI specification at `/openapi.json`.

To export the current specification to the project root, start the API and run:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/openapi.json -OutFile openapi.json
```

Regenerate the file whenever the API contract changes.

## Design Decisions

- FastAPI provides automatic request validation and interactive API documentation.
- HTTPX is used for upstream HTTP requests.
- Pydantic models define the expected meter response structure.
- Environment variables keep portal configuration and session credentials outside source code.
- A dedicated client separates upstream communication from route handling.
- The API is read-only and does not implement portal write operations.

## Assumptions and Limitations

- The observed meter-search endpoint is used as the upstream data source.
- The response model reflects the meter fields observed during portal inspection.
- Authentication depends on an authorized, valid session cookie.
- Full pagination semantics, search rules, rate limits, and other portal endpoints have not been fully verified.
- The API does not currently implement automatic session renewal or retry policies.

## Future Improvements

- Implement an approved login or session-renewal mechanism.
- Add stronger response validation and more comprehensive tests.
- Document and test pagination behavior.
- Add structured logging and request correlation IDs.
- Add retry and timeout policies appropriate for the upstream service.
- Add continuous integration to run tests automatically.

## Security

Never commit real credentials, cookies, tokens, or `.env` files. Only use authorized portal access and sanitized example data in documentation.
