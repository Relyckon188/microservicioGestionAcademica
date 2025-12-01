import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from app.config import config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cache = Cache()

def create_app() -> Flask:
    app_context = os.getenv('FLASK_CONTEXT', 'development')

    app = Flask(__name__)
    app.config.from_object(config.factory(app_context))

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cache.init_app(app)

    from app.resources import all_blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp, url_prefix="/api/v1")

    return app
