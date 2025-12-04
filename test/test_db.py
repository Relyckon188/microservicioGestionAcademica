from sqlalchemy import text
from app import db

def test_db_connection(app):
    result = db.session.query(text("'Hello world'")).one()
    assert result[0] == "Hello world"
