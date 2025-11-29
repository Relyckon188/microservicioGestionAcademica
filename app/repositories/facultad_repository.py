from app import db
from models.facultad import Facultad

class FacultadRepository:

    @staticmethod
    def get_all():
        return Facultad.query.all()

    @staticmethod
    def get_by_id(fid: int):
        return Facultad.query.get(fid)

    @staticmethod
    def create(data: dict):
        obj = Facultad(**data)
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def update(obj: Facultad, data: dict):
        for key, value in data.items():
            setattr(obj, key, value)
        db.session.commit()
        return obj

    @staticmethod
    def delete(obj: Facultad):
        db.session.delete(obj)
        db.session.commit()
