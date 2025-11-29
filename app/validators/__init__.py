from functools import wraps
from flask import request, jsonify

def validate_with(schema):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            json_data = request.get_json()
            if not json_data:
                return jsonify({"error": "Se requiere JSON"}), 400

            obj = schema.load(json_data)
            return fn(obj, *args, **kwargs)
        return wrapper
    return decorator
