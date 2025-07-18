import re
from typing import List, Tuple

# Match "package==1.0.0" or "package>=1.0,<2.0"
RE_DEPENDENCY = re.compile(r"^\s*(?P<name>[a-zA-Z0-9_\-\.]+)\s*(?P<specifier>[^#\s]+)?")


def parse_requirements(content: str) -> List[Tuple[str, str]]:
    """
    Parses the contents of a requirements.txt-like file and extracts
    package names and version specifiers."""
    dependencies = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        match = RE_DEPENDENCY.match(line)
        if match:
            name = match.group("name")
            specifier = match.group("specifier") or ""
            dependencies.append((name, specifier.strip()))
        else:
            print(f"[WARN] Ignored line: {line}")

    return dependencies
