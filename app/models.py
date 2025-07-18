from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class Severity(BaseModel):
    type: str
    score: str


class Vulnerability(BaseModel):
    id: str = Field(..., description="Unique vulnerability identifier")
    summary: Optional[str] = None
    severity: Optional[List[Severity]] = Field(
        default_factory=list, description="Severity levels"
    )
    fixed_versions: Optional[List[str]] = Field(default_factory=list)


class Dependency(BaseModel):
    name: str = Field(..., description="Package name")
    version: str
    vulnerabilities: List[Vulnerability] = Field(default_factory=list)


class Project(BaseModel):
    id: UUID
    name: str = Field(..., description="Project name")
    description: Optional[str] = None
    dependencies: List[Dependency] = Field(default_factory=list)


class ProjectWithVuln(Project):
    vulnerable: bool = Field(
        default=False, description="Indicates if the project has vulnerabilities"
    )
