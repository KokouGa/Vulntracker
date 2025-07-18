import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_scan_requirements():
    test_content = b"""
    flask==2.2.0
    requests==2.28.0
    """

    files = {"file": ("requirements.txt", test_content, "text/plain")}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/dependencies/scan", files=files)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(pkg["package"] == "flask" for pkg in data)
    assert all("vulnerabilities" in pkg for pkg in data)


@pytest.mark.asyncio
async def test_list_all_dependencies():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/dependencies/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "name" in data[0]
        assert "project_count" in data[0]
        assert "vulnerable" in data[0]


@pytest.mark.asyncio
async def test_get_dependency_detail():
    # dependency name to test
    test_content = b"requests==2.28.0"
    files = {"requirements_file": ("requirements.txt", test_content, "text/plain")}
    data = {"name": "TestDepProject", "description": "Testing dependency detail"}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/projects/", data=data, files=files)
        # Get the dependency details
        response = await client.get("/dependencies/requests")

    assert response.status_code == 200
    data = response.json()
    assert data["name"].lower() == "requests"
    assert isinstance(data["used_in"], list)
    assert "project_id" in data["used_in"][0]
