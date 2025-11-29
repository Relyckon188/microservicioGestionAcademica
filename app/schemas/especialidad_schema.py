from app import ma
from models.especialidad import Especialidad

class EspecialidadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Especialidad
        include_fk = True
        load_instance = True

especialidad_schema = EspecialidadSchema()
especialidades_schema = EspecialidadSchema(many=True)
