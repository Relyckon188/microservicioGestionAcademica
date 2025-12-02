from app.repositories.especialidad_repository import EspecialidadRepository
from app.repositories.facultad_repository import FacultadRepository

class EspecialidadService:

    @staticmethod
    def obtener_todas():
        return EspecialidadRepository.get_all()

    @staticmethod
    def obtener_por_id(eid: int):
        return EspecialidadRepository.get_by_id(eid)

    @staticmethod
    def crear_especialidad(data: dict):
        # Validar facultad existente
        if not FacultadRepository.get_by_id(data["facultad_id"]):
            raise ValueError("Facultad no existe")
        return EspecialidadRepository.create(data)

    @staticmethod
    def actualizar_especialidad(eid: int, data: dict):
        obj = EspecialidadRepository.get_by_id(eid)
        if not obj:
            return None
        return EspecialidadRepository.update(obj, data)

    @staticmethod
    def eliminar_especialidad(eid: int):
        obj = EspecialidadRepository.get_by_id(eid)
        if not obj:
            return None
        EspecialidadRepository.delete(obj)
        return obj
