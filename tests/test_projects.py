import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from app.main import app

@pytest.mark.asyncio
async def test_create_and_list_projects(tmp_path):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("requests==2.28.0\nflask==2.2.0")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        with req_file.open("rb") as f:
            response = await client.post(
                "/projects/",
                files={"requirements_file": ("requirements.txt", f, "text/plain")},
                data={"name": "My Test Project", "description": "Test project"}
            )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "My Test Project"
        assert isinstance(data["dependencies"], list)

        response = await client.get("/projects/")
        assert response.status_code == status.HTTP_200_OK
        projects = response.json()
        assert any(p["name"] == "My Test Project" for p in projects)
