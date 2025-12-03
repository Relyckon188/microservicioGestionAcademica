from marshmallow import Schema, fields, post_load, validate
from app.models.universidad import Universidad
from markupsafe import escape

class UniversidadMapping(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    sigla = fields.Str(required=True, validate=validate.Length(min=1, max=10))

    @post_load
    def nueva_universidad(self, data, **kwargs):
        for key in ['nombre', 'sigla']:
            if key in data and isinstance(data[key], str):
                data[key] = str(escape(data[key]))
        return Universidad(**data)