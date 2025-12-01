from app import db
from app.models.especialidad import Especialidad

class EspecialidadRepository:

    @staticmethod
    def get_all():
        return Especialidad.query.all()

    @staticmethod
    def get_by_id(eid: int):
        return Especialidad.query.get(eid)

    @staticmethod
    def create(data: dict):
        obj = Especialidad(**data)
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def update(obj: Especialidad, data: dict):
        for key, value in data.items():
            setattr(obj, key, value)
        db.session.commit()
        return obj

    @staticmethod
    def delete(obj: Especialidad):
        db.session.delete(obj)
        db.session.commit()
