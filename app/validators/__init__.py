from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError

def validate_with(schema_class):
    """
    Decorador para validar request JSON con un Schema (clase).
    Uso:
       @validate_with(EspecialidadMapping)
       def crear(...):
           ...
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                schema = schema_class()
                # load lanzará ValidationError si no valida
                valid = schema.load(request.get_json())
                # adjuntar datos validados en request (opcional)
                request.validated_json = valid
            except ValidationError as err:
                return jsonify({"errors": err.messages}), 400
            return f(*args, **kwargs)
        return wrapped
    return decorator
