from app.repositories.facultad_repository import FacultadRepository
from app.repositories.universidad_repository import UniversidadRepository

class FacultadService:

    @staticmethod
    def obtener_todas():
        return FacultadRepository.get_all()

    @staticmethod
    def obtener_por_id(fid: int):
        return FacultadRepository.get_by_id(fid)

    @staticmethod
    def crear_facultad(data: dict):
        # Validar universidad existente
        if not UniversidadRepository.get_by_id(data["universidad_id"]):
            raise ValueError("Universidad no existe")
        return FacultadRepository.create(data)

    @staticmethod
    def actualizar_facultad(fid: int, data: dict):
        obj = FacultadRepository.get_by_id(fid)
        if not obj:
            return None
        return FacultadRepository.update(obj, data)

    @staticmethod
    def eliminar_facultad(fid: int):
        obj = FacultadRepository.get_by_id(fid)
        if not obj:
            return None
        FacultadRepository.delete(obj)
        return obj
