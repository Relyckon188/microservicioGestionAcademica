import logging
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from app.config.config import factory
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_hashids import Hashids

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app() -> Flask:
    app_context = os.getenv('FLASK_CONTEXT', 'development')

    app = Flask(__name__)

    config_obj = factory(app_context)
    app.config.from_object(config_obj)

    db.init_app(app)
    ma.init_app(app)

    from models import Universidad, Facultad, Especialidad

    migrate.init_app(app, db)

    from app.resources import universidad_bp
    app.register_blueprint(universidad_bp, url_prefix="/api/v1")

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
