from marshmallow import Schema, fields, post_load, validate
from app.models.facultad import Facultad
from markupsafe import escape

class FacultadMapping(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True, validate=validate.Length(max=100))
    abreviatura = fields.Str(required=True, validate=validate.Length(max=10))
    directorio = fields.Str(required=True, validate=validate.Length(max=100))
    sigla = fields.Str(required=True, validate=validate.Length(max=10))
    codigopostal = fields.Str(validate=validate.Length(max=10))
    ciudad = fields.Str(validate=validate.Length(max=50))
    domicilio = fields.Str(validate=validate.Length(max=100))
    telefono = fields.Str(validate=validate.Length(max=20))
    contacto = fields.Str(validate=validate.Length(max=100))
    email = fields.Email(required=True)

    universidad_id = fields.Int(required=True)

    @post_load
    def make_facultad(self, data, **kwargs):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = escape(value)
        return Facultad(**data)
