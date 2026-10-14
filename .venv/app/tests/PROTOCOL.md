# Urja Meter Ops — Portal Protocol Notes

## 1. Overview

This document records the observed behavior of the Urja Meter Ops portal used as the upstream data source for the Flock Energy Meter API.

Portal URL: https://urja-ops.flockenergy.tech

The portal provides meter information through HTTP requests. These notes are based on browser inspection and observed network responses. They describe only behavior that has been verified during exploration.

## 2. Authentication

- The portal requires an authenticated session to access meter data.
- The browser sends a session cookie with requests to the portal.
- The observed session cookie name is `__Secure-better-auth.session_token`.
- Requests made without a valid session may fail or redirect, depending on the portal's authentication behavior.
- Session cookies are sensitive credentials and must not be committed to source control or included in logs, screenshots, or documentation.

The current implementation accepts the session cookie through the `URJA_PORTAL_SESSION_COOKIE` environment variable.

**Limitation:** The current implementation relies on a manually supplied session cookie. It does not implement a complete login flow or automatic session renewal.

## 3. Observed Meter Search Endpoint

### Request

- Method: `GET`
- Path: `/portal/meters/search`
- Example URL: `/portal/meters/search?q=&page=1`
- Query parameters:
  - `q`: Search query; an empty value was observed when listing meters.
  - `page`: Page number; `1` was observed in the inspected request.

### Request Headers

The browser request included:

- `Accept: */*`
- An authenticated session cookie
- A referer pointing to the portal's meters page

The session cookie value is intentionally omitted because it is sensitive.

### Observed Response

- Status: `200 OK`
- Content type: `application/json`
- A response body containing a top-level `data` array was observed.

A sanitized example of the observed response structure is:

```json
{
  "data": [
    {
      "meterId": "J100000",
      "serialNo": "SE33962",
      "make": "HPL",
      "phaseType": "single",
      "installStatus": "Decommissioned",
      "dtCode": "DT-001"
    }
  ]
}
```

This is a representative excerpt, not the complete portal response. The example values come from the inspected response.

## 4. Observed Meter Fields

| Field | Observed meaning |
|---|---|
| `meterId` | Meter identifier |
| `serialNo` | Meter serial number |
| `make` | Meter manufacturer or make |
| `phaseType` | Phase classification |
| `installStatus` | Installation status |
| `dtCode` | Distribution transformer code |

The field meanings above are inferred from their names and observed values. They have not been independently confirmed against formal portal documentation.

## 5. Integration Design

The local API uses the following components:

- `app/config.py`: Loads configuration from environment variables.
- `app/portal_client.py`: Sends HTTP requests to the upstream portal and validates the response structure.
- `app/schemas.py`: Defines the Pydantic model for meter responses.
- `app/main.py`: Exposes the FastAPI routes.

The upstream request uses the observed meter-search path and passes `q` and `page` as query parameters.

The integration checks for authentication failures, HTTP errors, non-JSON responses, and unexpected response structures.

## 6. Local API Mapping

The local API exposes:

- `GET /` — Returns basic service information.
- `GET /health` — Returns the service health status.
- `GET /api/v1/meters` — Retrieves meter data through the upstream meter-search endpoint.

The local meter endpoint accepts `q` and `page` query parameters and returns a structured response containing a `data` array.

Upstream failures are surfaced as HTTP `502 Bad Gateway` responses.

## 7. Read-Only Behavior

The current integration performs only a `GET` request to retrieve meter search results. It does not create, modify, or delete portal records.

No write operations have been implemented.

## 8. Known Limitations and Unverified Behavior

- Authentication depends on a valid session cookie supplied through environment configuration.
- Automatic login, session refresh, and cookie renewal are not implemented.
- The portal's complete pagination behavior has not yet been documented.
- Search matching rules and supported search fields have not been independently verified.
- The complete meter response schema has not been established.
- Rate limits, retry policies, and upstream availability guarantees have not been verified.
- Other portal endpoints have not been documented unless explicitly inspected.

These points should be treated as unknown rather than assumed portal behavior.

## 9. Security Considerations

- Keep `.env` out of version control.
- Use `.env.example` only for placeholder configuration.
- Never commit real passwords, session cookies, or access tokens.
- Avoid logging sensitive request headers.
- Use a dedicated, authorized test account or approved authentication method where available.

## 10. Further Investigation

Before extending the integration, investigate:

1. The portal's supported login and session-renewal mechanism.
2. Pagination metadata and behavior for additional pages.
3. Search behavior for known meter identifiers and serial numbers.
4. Optional and required fields in the complete response schema.
5. Error responses for unauthenticated requests and invalid query parameters.
6. Any documented rate limits or operational constraints.