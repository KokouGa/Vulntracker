
from fastapi import FastAPI
from app.routes.dependencies import router as dependencies_router
from app.routes.projects import router as projects_router
from app.routes.project_details import router as project_details_router

app = FastAPI(
    title="Project Dependency Vulnerability API",
    description="Track the dependencies and detect vulnerabilities using osv.dev.",
    version="1.0.0"
)

# Register routers
app.include_router(dependencies_router, prefix="/dependencies", tags=["Dependencies"])
app.include_router(projects_router, prefix="/projects", tags=["Projects"])
app.include_router(project_details_router)


