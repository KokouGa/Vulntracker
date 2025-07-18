import httpx
from app.cache import get_from_cache, set_to_cache
from typing import List, Dict, Tuple

OSV_API_URL = "https://api.osv.dev/v1/query"


class OSVClient:
    def __init__(self, base_url: str = OSV_API_URL, timeout: int = 10):
        """
        Initialize the OSVClient with a base URL
        """
        self.base_url = base_url
        self.timeout = timeout
        self.cache: Dict[Tuple[str, str], List[Dict]] = {}  # Cache to store results

    async def get_vulnerabilities(self, package_name: str, version: str) -> List[Dict]:
        """
        Send a POST request to OSV.dev to get vulnerabilities

        Args:
            package_name (str): The name of the Python package.
            version (str): The specific version.

        Returns:
            List[Dict]: A list of vulnerabilities returned by OSV.dev.
        """
        # Check cache first
        key = f"{package_name.lower().strip()}:{version.strip()}"
        cached = get_from_cache(key)
        if cached is not None:
            print(f"[CACHE HIT] {key}")
            return cached

        payload = {
            "version": version,
            "package": {"name": package_name, "ecosystem": "PyPI"},
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.base_url, json=payload)
                response.raise_for_status()
                data = response.json()
                vulns = data.get("vulns", [])

                # Cache the result
                set_to_cache(key, vulns)

                return vulns
        except httpx.HTTPError as e:
            # Handle HTTP errors (e.g., network issue, timeout, 5xx from API)
            print(f"[OSVClient Error] {package_name}=={version} → {e}")
            return []

    def format_vulnerabilities(self, vulns: list[dict]) -> list[str]:

        def format_one(vuln: dict) -> str:
            id_ = vuln.get("id", "N/A")
            summary = vuln.get("summary", "No summary")
            severity = vuln.get("database_specific", {}).get("severity", "Unknown")
            published = vuln.get("published", "Unknown date")
            affected_versions = (
                ", ".join(vuln.get("affected", [{}])[0].get("versions", []))
                if vuln.get("affected")
                else "N/A"
            )
            references = [
                ref["url"] for ref in vuln.get("references", []) if "url" in ref
            ]
            ref_str = "\n".join(references)
            return (
                f"ID: {id_}\n"
                f"Summary: {summary}\n"
                f"Severity: {severity}\n"
                f"Published: {published}\n"
                f"Affected Versions: {affected_versions}\n"
                f"References:\n{ref_str}\n" + "-" * 40
            )

        return [format_one(v) for v in vulns]
