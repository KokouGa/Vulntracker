from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict
from app.parser import parse_requirements
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
