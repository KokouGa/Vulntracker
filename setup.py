from setuptools import setup, find_packages

setup(
    name="vulntracker",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "httpx",
        "uvicorn",
        "python-multipart",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-asyncio",
            "flake8",
            "black",
            "mypy",
        ]
    },
    entry_points={
        "console_scripts": [
            "vulntracker=app.main:app",
        ],
    },
)
