from fastapi import APIRouter, HTTPException
from app.routes.projects import projects_db


router = APIRouter()


@router.get("/projects/{project_id}/dependencies")
async def get_project_dependencies(project_id: str):
    """
    Get dependencies for  specific project.
    Returns a list of dependencies with their vulnerability status.
    """
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    results = []
    for dep in project.dependencies:
        is_vulnerable = len(dep.vulnerabilities) > 0
        results.append(
            {
                "name": dep.name,
                "version": dep.version,
                "vulnerable": is_vulnerable,
                "vulnerabilities": dep.vulnerabilities,
            }
        )

    return {
        "project_id": project_id,
        "project_name": project.name,
        "dependencies": results,
    }
