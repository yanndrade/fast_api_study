#!/bin/sh

# Execute the Alembic migration tool to upgrade the database
poetry run alembic upgrade head

# Run the FastAPI application using Uvicorn
poetry run uvicorn --host 0.0.0.0 fastapizero.app:app