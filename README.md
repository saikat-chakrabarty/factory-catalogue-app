# Production-Ready FastAPI Template

A production-ready FastAPI project template that follows modern software engineering practices. It features a monorepo structure with shared libraries, deterministic dependency management, structured logging, middleware for observability, robust API design, PostgreSQL integration with Alembic migrations, and comprehensive testing support.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Development Workflow](#development-workflow)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Contributing](#contributing)


## Development Workflow
# Pre-commit Hooks: Pre-commit hooks ensure code quality. They run automatically before commits. To install the hooks, run:
pre-commit install

# Code Formatting & Linting:
Format code: black .
Lint code: flake8 .
Type-check: mypy .

## Running the Application
# Set Up Environment Variables:

Copy the example file and modify as needed:
cp .env.example .env_<environment>

# Install Dependencies:
Using Poetry:
pyenv local 3.13.1
poetry env use /usr/bin/python3.1
poetry env info
poetry install
Or, with pip:
pip3 install -r requirements.txt

# Run Database Migrations:

After updating the models, generate and apply an Alembic migration:
alembic revision --autogenerate -m "Add raw_materials and association table"
alembic upgrade head

# Run the Admin App:
source venv/bin/activate
uvicorn apps.admin_app.main:app --reload --port 8000

# Run the Search App (in a separate terminal):
source venv/bin/activate
uvicorn apps.search_app.main:app --reload --port 8001

# Login to DB
sudo su - postgres
psql 

# Get API doc
http://localhost:8000/docs#/
http://localhost:8001/docs#/


## Project Structure
production-fastapi-template/
├── apps/
│   ├── admin_app/                   # Admin app for adding factory details
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       └── factories.py
│   |       └── health.py
│   └── search_app/                  # Search app for querying factories
│       ├── __init__.py
│       ├── main.py
│       └── routes/
│           └── factories.py
│           └── health.py
├── libs/
│   ├── common/                      # Shared configuration, logging, DB, middleware, etc.
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── logging.py
│   │   ├── db.py
│   │   ├── middleware.py
│   │   └── exceptions.py
│   └── catalog/                     # Shared domain objects for the factory catalogue
│       ├── __init__.py
│       ├── db.py
│       ├── models.py
│       └── schemas.py
│   └── utils/                      # Shared utility functions
│       ├── __init__.py
│       ├── helper.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_app.py
├── alembic/                         # Database migration scripts (Alembic)
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── .env.example
├── pyproject.toml
├── requirements.txt
├── pre-commit-config.yaml
└── README.md
