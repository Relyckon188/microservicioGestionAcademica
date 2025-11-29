import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from app.config.config import config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app() -> Flask:
    app_context = os.getenv('FLASK_CONTEXT', 'development')

    app = Flask(__name__)
    app.config.from_object(config.factory(app_context))

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Registrar Blueprints
    from app.resources.universidad_resource import universidad_bp
    from app.resources.facultad_resource import facultad_bp
    from app.resources.especialidad_resource import especialidad_bp

    app.register_blueprint(universidad_bp, url_prefix="/api/v1")
    app.register_blueprint(facultad_bp, url_prefix="/api/v1")
    app.register_blueprint(especialidad_bp, url_prefix="/api/v1")

    return app
