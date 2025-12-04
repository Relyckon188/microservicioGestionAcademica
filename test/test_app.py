from flask import current_app

def test_app_inicial(app):
    assert current_app is not None
