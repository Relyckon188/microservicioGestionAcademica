from app import db
from app.models.universidad import Universidad

class UniversidadRepository:

    @staticmethod           #no usa self
    def get_all():                                      #session actua como "puente" de db
        return db.session.query(Universidad).all()      #SELECT completa

    @staticmethod
    def get_by_id(uid: int):
        return db.session.get(Universidad, uid)     #SELECT de solo un registro con WHERE uid = (algo)
    
    @staticmethod
    def create(data: dict):         #dict: diccionario, es un tipo de data
        obj = Universidad(**data)   #sin el dict se escribe: Universidad(nombre=data.nombre, sigla=data.sigla)
        db.session.add(obj)         #inserta los datos y queda pendiente
        db.session.commit()         #ejecuta el INSERT en la tabla
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
