from app import db
from app.models.especialidad import Especialidad

class EspecialidadRepository:

    @staticmethod
    def get_all():
        return db.session.query(Especialidad).all()

    @staticmethod
    def get_by_id(eid: int):
        return db.session.get(Especialidad, eid)

    @staticmethod
    def create(obj: Especialidad):
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def update(obj: Especialidad, data: Especialidad):
        for attr in ["nombre", "letra", "observacion", "facultad_id"]:
            valor = getattr(data, attr, None)
            setattr(obj, attr, valor)

        db.session.commit()
        return obj

    @staticmethod
    def delete(obj: Especialidad):
        db.session.delete(obj)
        db.session.commit()
