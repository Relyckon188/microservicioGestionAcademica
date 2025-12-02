from app import db
from app.models.facultad import Facultad

class FacultadRepository:

    @staticmethod
    def get_all():
        return Facultad.query.all()

    @staticmethod
    def get_by_id(fid: int):
        return Facultad.query.get(fid)

    @staticmethod
    def create(facultad_obj):
        db.session.add(facultad_obj)
        db.session.commit()
        return facultad_obj

    @staticmethod
    def update(facultad_obj):
        db.session.commit()
        return facultad_obj

    @staticmethod
    def delete(facultad_obj):
        db.session.delete(facultad_obj)
        db.session.commit()
