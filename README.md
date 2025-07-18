# Project Dependency Vulnerability API

#  VulnTracker – Python Project Vulnerability Tracker

**VulnTracker** is an API (FastApi) designed to analyze `requirements.txt` files of Python projects and detect vulnerable dependencies using [OSV.dev](https://osv.dev/) public vulnerability database.


---

##  Project Goals

-  Analyze Python project dependencies.
-  Detect known vulnerabilities via OSV.dev API.
-  Manage multiple projects and their dependencies.
-  Implement caching to reduce redundant API calls.
-  Provide clean, tested, and verified code using quality tools.

---

##  Features

| Feature                  | Description                                                        |
|--------------------------|--------------------------------------------------------------------|
|  **Project Creation**   | Upload a `requirements.txt` and parse dependencies.               |
|  **Vulnerability Scan**| Query OSV.dev for security issues.                                |
|  **Dependency Listing**| Display all known dependencies.                                   |
|  **Package Details**   | Return CVEs for a specific package.                               |
|  **In-Memory Caching**  | Uses `cachetools` for faster response times.                      |
|  **Unit Tests**         | Coverage provided via `pytest`.                                   |
|  **Code Quality**       | Linting (`flake8`), format (`black`), type check (`mypy`). |
|  **Automation**         | Fully integrated with `tox` for streamlined validation.           |

---

##  Tech Stack

- **Python 3.10**
- **FastAPI** – Web framework
- **Uvicorn** – ASGI server
- **CacheTools** – TTL-based caching
- **Pytest** – Testing framework
- **Black** – Code formatter
- **Flake8** – Linting tool
- **Mypy** – Static type checker
- **Tox** – Environment automation

---

##  API Endpoints

| Method | Route                     | Description                                  |
|--------|---------------------------|----------------------------------------------|
| POST   | `/projects/`              | Upload a `requirements.txt` file             |
| GET    | `/projects/`              | List all projects and their vulnerability status |
| GET    | `/projects/{id}`          | Show dependencies for a specific project     |
| GET    | `/dependencies/`          | List all known dependencies                  |
| GET    | `/dependencies/{name}`    | Show CVEs for a specific package             |

##  Installation & Usage

```bash
git clone https://github.com/KokouGa/Vulntracker
cd vulntracker

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt -r requirements-dev.txt

python run.py  
 or 
uvicorn app.main:app --reload
