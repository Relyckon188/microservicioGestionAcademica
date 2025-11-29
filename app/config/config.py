import os
from pathlib import Path
from dotenv import load_dotenv

# Directorio base del proyecto
basedir = Path(__file__).resolve().parents[2]

# Cargar .env
load_dotenv(basedir / ".env")


class Config:
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI")


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI")


def factory(env: str) -> Config:
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestConfig,
    }
    return config_map.get(env, DevelopmentConfig)
