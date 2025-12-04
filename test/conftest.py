import os
import pytest

from app import create_app, db


@pytest.fixture
def app():
    os.environ["FLASK_CONTEXT"] = "testing"
    app = create_app()

    ctx = app.app_context()
    ctx.push()

    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    ctx.pop()

