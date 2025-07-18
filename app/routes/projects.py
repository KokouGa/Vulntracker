from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from app.parser import parse_requirements
from app.osv_client import OSVClient
from app.models import Project, Dependency, Vulnerability, ProjectWithVuln 
import asyncio
import uuid

router = APIRouter()
osv_client = OSVClient()

# In-memory storage
projects_db: dict[str, Project] = {}

@router.post("/", response_model=Project)
async def create_project(
    name: str = Form(...),
    description: str = Form(""),
    requirements_file: UploadFile = File(...)
) -> Project:
    """
    Create  new project with a requirements.txt.
    Parses the dependencies, checks vulnerabilities, and stores the project in memory.
    """
    if not requirements_file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are accepted.")

    try:
        content = await requirements_file.read()
        requirements = parse_requirements(content.decode())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse requirements: {e}")

    # Async query to OSV for each dependency
    async def query(name: str, version: str) -> Dependency:
        vulns_data = await osv_client.get_vulnerabilities(name, version)
        vulns = [Vulnerability(**v) for v in vulns_data]
        return Dependency(name=name, version=version, vulnerabilities=vulns)

    tasks = [query(name, version) for name, version in requirements]
    dependencies: List[Dependency] = await asyncio.gather(*tasks)

    project_id = str(uuid.uuid4())
    project = Project(id=project_id, name=name, description=description, dependencies=dependencies)
    projects_db[project_id] = project
    return project

@router.get("/", response_model=List[ProjectWithVuln])
async def get_all_projects():
    """
    Get all projects with their vulnerable status.
    """
    result: List[ProjectWithVuln] = []

    for project in projects_db.values():
        is_vulnerable = any(dep.vulnerabilities for dep in project.dependencies)
        result.append(ProjectWithVuln(**project.model_dump(), vulnerable=is_vulnerable))

    return result