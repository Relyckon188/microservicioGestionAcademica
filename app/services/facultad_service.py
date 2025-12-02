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
    def crear_facultad(facultad_obj):
        # Validar universidad
        if not UniversidadRepository.get_by_id(facultad_obj.universidad_id):
            raise ValueError("Universidad no existe")

        return FacultadRepository.create(facultad_obj)

    @staticmethod
    def actualizar_facultad(fid: int, facultad_obj):
        existente = FacultadRepository.get_by_id(fid)
        if not existente:
            return None

        # Actualizar campo por campo
        existente.nombre = facultad_obj.nombre
        existente.abreviatura = facultad_obj.abreviatura
        existente.directorio = facultad_obj.directorio
        existente.sigla = facultad_obj.sigla
        existente.codigopostal = facultad_obj.codigopostal
        existente.ciudad = facultad_obj.ciudad
        existente.domicilio = facultad_obj.domicilio
        existente.telefono = facultad_obj.telefono
        existente.contacto = facultad_obj.contacto
        existente.email = facultad_obj.email
        existente.universidad_id = facultad_obj.universidad_id

        return FacultadRepository.update(existente)

    @staticmethod
    def eliminar_facultad(fid: int):
        existente = FacultadRepository.get_by_id(fid)
        if not existente:
            return None

        FacultadRepository.delete(existente)
        return existente
