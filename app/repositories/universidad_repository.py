from app import db
from app.models.universidad import Universidad

class UniversidadRepository:

    @staticmethod
    def get_all():
        return Universidad.query.all()

    @staticmethod
    def get_by_id(uid: int):
        return Universidad.query.get(uid)

    @staticmethod
    def create(data: dict):
        obj = Universidad(**data)
        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def update(obj: Universidad, data: dict):
        for key, value in data.items():
            setattr(obj, key, value)
        db.session.commit()
        return obj

    @staticmethod
    def delete(obj: Universidad):
        db.session.delete(obj)
        db.session.commit()
