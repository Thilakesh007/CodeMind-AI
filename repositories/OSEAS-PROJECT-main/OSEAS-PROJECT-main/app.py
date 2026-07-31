"""WSGI entry point.

Only initializes the Flask application via the factory in backend/__init__.py.
No routes, HTML, CSS, JS, or business logic live in this file — all of that
has been moved into backend/, frontend/, database/, and ai/.

For local development, run `python run.py` instead (it configures host/port
from config.py). This file exists for WSGI servers (gunicorn/uwsgi) that
expect an `app` object at the project root, e.g.:
    gunicorn app:app
"""
from backend import create_app

app = create_app()
