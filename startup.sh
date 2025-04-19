#!/bin/bash
python -m alembic upgrade head
exec gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:${PORT:-8000}