import httpx

from app.config import settings


class PortalClientError(Exception):
    """Raised when the upstream portal cannot provide usable data."""


class PortalClient:
    def __init__(self):
        self.client = httpx.Client(
            base_url=settings.base_url,
            timeout=httpx.Timeout(15.0, connect=5.0),
            follow_redirects=True,
        )

        if settings.session_cookie:
            self.client.headers["Cookie"] = settings.session_cookie

    def search_meters(self, query: str = "", page: int = 1) -> dict:
        if not settings.session_cookie:
            raise PortalClientError(
                "Portal session cookie is not configured."
            )

        try:
            response = self.client.get(
                "/portal/meters/search",
                params={"q": query, "page": page},
            )

            if response.status_code in (401, 403):
                raise PortalClientError(
                    "Portal authentication failed or the session expired."
                )

            response.raise_for_status()
            payload = response.json()

            if not isinstance(payload, dict) or not isinstance(
                payload.get("data"), list
            ):
                raise PortalClientError(
                    "Portal returned an unexpected response structure."
                )

            return payload

        except PortalClientError:
            raise
        except (httpx.HTTPError, ValueError) as exc:
            raise PortalClientError(
                "Unable to retrieve valid meter data from the portal."
            ) from exc

    def close(self):
        self.client.close()
