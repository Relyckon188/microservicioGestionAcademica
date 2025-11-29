from marshmallow import Schema, fields, post_load, validate
from app.models.especialidad import Especialidad
from markupsafe import escape

class EspecialidadMapping(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(max=100))
    letra = fields.Str(required=True, validate=validate.Length(equal=1))
    observacion = fields.Str(validate=validate.Length(max=255))

    facultad_id = fields.Int(required=True)

    @post_load
    def make_especialidad(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = escape(value)
        return Especialidad(**data)
