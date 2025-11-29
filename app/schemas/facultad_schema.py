from app import ma
from models.facultad import Facultad

class FacultadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Facultad
        include_fk = True
        load_instance = True

facultad_schema = FacultadSchema()
facultades_schema = FacultadSchema(many=True)
