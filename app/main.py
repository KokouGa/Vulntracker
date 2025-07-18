
from fastapi import FastAPI
from app.routes.dependencies import router as dependencies_router
from app.routes.projects import router as projects_router
from app.routes.project_details import router as project_details_router

app = FastAPI(
    title="Project Dependency Vulnerability API",
    description="Track the dependencies and detect vulnerabilities using osv.dev.",
    version="1.0.0"
)

# wellcome route 
@app.get("/", tags=["Welcome"])
async def welcome():
    return {
                "message": "Welcome to the Project Dependency Vulnerability API!",
                "api": {
                    "version": "1.0.0",
                    "documentation_url": "/docs",
                    "author": "Kokou Gawonou"
                    },
                "endpoints": {
                    "projects": "/projects/",
                    "dependencies": "/dependencies/"
                    }
        }


# Register routers
app.include_router(projects_router, prefix="/projects", tags=["Projects"])
app.include_router(project_details_router)
app.include_router(dependencies_router, prefix="/dependencies", tags=["Dependencies"])



