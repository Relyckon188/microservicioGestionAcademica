from app.repositories.universidad_repository import UniversidadRepository

class UniversidadService:

    @staticmethod
    def listar():
        return UniversidadRepository.get_all()

    @staticmethod
    def obtener(uid: int):
        return UniversidadRepository.get_by_id(uid)

    @staticmethod
    def crear(data: dict):
        return UniversidadRepository.create(data)

    @staticmethod
    def actualizar(uid: int, data: dict):
        obj = UniversidadRepository.get_by_id(uid)
        if not obj:
            return None
        return UniversidadRepository.update(obj, data)

    @staticmethod
    def eliminar(uid: int):
        obj = UniversidadRepository.get_by_id(uid)
        if not obj:
            return None
        UniversidadRepository.delete(obj)
        return obj
