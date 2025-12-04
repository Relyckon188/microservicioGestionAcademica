import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parents[2]

load_dotenv(basedir / ".env")


class Config:
    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False

    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI")


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def factory(env: str):
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestConfig,
    }

    return config_map.get(env, DevelopmentConfig)
