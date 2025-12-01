from app import ma
from app.models.universidad import Universidad

class UniversidadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Universidad
        include_fk = True
        load_instance = True

universidad_schema = UniversidadSchema()
universidades_schema = UniversidadSchema(many=True)
