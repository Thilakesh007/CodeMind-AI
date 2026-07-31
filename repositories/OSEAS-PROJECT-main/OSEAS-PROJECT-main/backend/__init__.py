"""Application factory.

Replaces the single global `app = Flask(__name__)` plus scattered route
registrations in the original app.py. The Flask app now only initializes
Flask, loads configuration, sets up logging, and registers Blueprints —
no HTML/CSS/JS/business logic lives here.
"""
from flask import Flask

from config import config_by_name
from backend.utils.logger import configure_logging, get_logger


def create_app(config_name: str = "default") -> Flask:
    config_class = config_by_name[config_name]

    app = Flask(
        __name__,
        template_folder=config_class.TEMPLATE_FOLDER,
        static_folder=config_class.STATIC_FOLDER,
    )
    app.config.from_object(config_class)

    # Session cookie settings required for ngrok / HTTPS sessions (unchanged from app.py).
    app.secret_key = config_class.SECRET_KEY
    app.config.update(
        SESSION_COOKIE_SAMESITE=config_class.SESSION_COOKIE_SAMESITE,
        SESSION_COOKIE_SECURE=config_class.SESSION_COOKIE_SECURE,
    )

    configure_logging(config_class.LOG_FILE)
    logger = get_logger(__name__)
    logger.info("FULL AI ENGAGEMENT SYSTEM RUNNING")  # replaces the original print()

    _register_blueprints(app)

    return app


def _register_blueprints(app: Flask) -> None:
    from backend.routes.auth_routes import auth_bp
    from backend.routes.student_routes import student_bp
    from backend.routes.faculty_routes import faculty_bp
    from backend.routes.metrics_routes import metrics_bp
    from backend.routes.api_routes import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(api_bp)
