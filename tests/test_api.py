from fastapi.testclient import TestClient

from app.main import app, portal
from app.portal_client import PortalClientError

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_meters_success(monkeypatch):
    sample_data = {
        "data": [
            {
                "meterId": "J100000",
                "serialNo": "SE33962",
                "make": "HPL",
                "phaseType": "single",
                "installStatus": "Decommissioned",
                "dtCode": "DT-001",
            }
        ]
    }

    def fake_search_meters(query="", page=1):
        assert query == ""
        assert page == 1
        return sample_data

    monkeypatch.setattr(portal, "search_meters", fake_search_meters)
    response = client.get("/api/v1/meters?q=&page=1")

    assert response.status_code == 200
    assert response.json()["data"][0]["meterId"] == "J100000"


def test_upstream_error_returns_502(monkeypatch):
    def fake_search_meters(query="", page=1):
        raise PortalClientError("Test upstream failure")

    monkeypatch.setattr(portal, "search_meters", fake_search_meters)
    response = client.get("/api/v1/meters")

    assert response.status_code == 502
    assert response.json()["detail"] == "Test upstream failure"


def test_invalid_page_returns_422():
    response = client.get("/api/v1/meters?page=0")
    assert response.status_code == 422
