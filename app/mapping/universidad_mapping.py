from marshmallow import Schema, fields, post_load, validate
from app.models.universidad import Universidad
from markupsafe import escape

class UniversidadMapping(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    sigla = fields.String(required=True, validate=validate.Length(min=1, max=10))
    tipo = fields.String(required=True, validate=validate.Length(min=1, max=50))  # opcional: validar tamaño máximo

    @post_load
    def nueva_universidad(self, data, **kwargs):
        for key in ['nombre', 'sigla', 'tipo']:
            if key in data and isinstance(data[key], str):
                data[key] = escape(data[key])
        return Universidad(**data)