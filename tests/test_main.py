import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app.main import app


@pytest.mark.asyncio
async def test_welcome_route():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Welcome to the Project Dependency Vulnerability API!"
    assert data["api"]["version"] == "1.0.0"
    assert data["api"]["author"] == "Kokou Gawonou"
    assert "documentation_url" in data["api"]

    assert data["endpoints"]["projects"] == "/projects/"
    assert data["endpoints"]["dependencies"] == "/dependencies/"


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "VulnTracker is healthy!"
    assert data["version"] == "1.0.0"
