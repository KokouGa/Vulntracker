from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict
from app.parser import parse_requirements
from app.routes.projects import projects_db
from app.osv_client import OSVClient
import asyncio

router = APIRouter()
osv_client = OSVClient()

@router.post("/scan")
async def scan_requirements(file: UploadFile = File(...)) -> List[Dict]:
    """
    Upload a requirements.txt file, parse dependencies and query OSV API for vulnerabilities.
    """
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Only text/plain files are accepted")
    
    content = await file.read()
    text = content.decode("utf-8")
    
    dependencies = parse_requirements(text)
    
    # Prepare tasks for async queries to OSV
    async def query_package(pkg):
        name, version = pkg
        vulns = await osv_client.get_vulnerabilities(name, version)
        return {"package": name, "version": version, "vulnerabilities": vulns}
    
    tasks = [query_package(dep) for dep in dependencies]
    results = await asyncio.gather(*tasks)
    
    return results
@router.get("/")
async def list_all_dependencies():
    """
    Lists all dependencies used the projects, if they are vulnerable.
    """
    dependency_stats = {}

    for project in projects_db.values():
        for dep in project.dependencies:
            key = dep.name.lower()
            if key not in dependency_stats:
                dependency_stats[key] = {
                    "name": dep.name,
                    "projects": set(),
                    "vulnerable": False
                }
            dependency_stats[key]["projects"].add(project.id)
            if dep.vulnerabilities:
                dependency_stats[key]["vulnerable"] = True

    result = []
    for dep in dependency_stats.values():
        result.append({
            "name": dep["name"],
            "project_count": len(dep["projects"]),
            "vulnerable": dep["vulnerable"]
        })

    return result


@router.get("/{dependency_name}")
async def get_dependency_detail(dependency_name: str):
    """
    the  detail information about a specific dependency in the  across projects.
    """
    used_in = []

    for project in projects_db.values():
        for dep in project.dependencies:
            if dep.name.lower() == dependency_name.lower():
                used_in.append({
                    "project_id": project.id,
                    "project_name": project.name,
                    "version": dep.version,
                    "vulnerable": bool(dep.vulnerabilities),
                    "vulnerabilities": dep.vulnerabilities
                })

    if not used_in:
        raise HTTPException(status_code=404, detail="Dependency not found")

    return {
        "name": dependency_name,
        "used_in": used_in
    }
