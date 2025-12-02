from app.repositories.universidad_repository import UniversidadRepository

class UniversidadService:

    @staticmethod
    def obtener_todas():
        return UniversidadRepository.get_all()

    @staticmethod
    def obtener_por_id(uid: int):
        return UniversidadRepository.get_by_id(uid)

    @staticmethod
    def crear_universidad(data: dict):
        return UniversidadRepository.create(data)

    @staticmethod
    def actualizar_universidad(uid: int, data: dict):
        obj = UniversidadRepository.get_by_id(uid)
        if not obj:
            return None
        return UniversidadRepository.update(obj, data)

    @staticmethod
    def eliminar_universidad(uid: int):
        obj = UniversidadRepository.get_by_id(uid)
        if not obj:
            return None
        UniversidadRepository.delete(obj)
        return obj
