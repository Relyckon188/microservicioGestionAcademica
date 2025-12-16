from app.repositories.facultad_repository import FacultadRepository
from app.repositories.universidad_repository import UniversidadRepository
from flask import current_app

class FacultadService:

    @staticmethod
    def obtener_todas():
        cache = current_app.extensions.get('cache')
        
        if cache:
            cached = cache.get('facultad:all')
            if cached:
                return cached
        
        facultades = FacultadRepository.get_all()
        
        if cache:
            cache.set('facultad:all', facultades, timeout=60)
        
        return facultades

    @staticmethod
    def obtener_por_id(fid: int):
        cache = current_app.extensions.get('cache')
        
        if cache:
            cached = cache.get(f'facultad:{fid}')
            if cached:
                return cached
        
        facultad = FacultadRepository.get_by_id(fid)
        
        if cache:
            cache.set(f'facultad:{fid}', facultad, timeout=60)
        
        return facultad

    @staticmethod
    def crear_facultad(facultad_obj):
        if not UniversidadRepository.get_by_id(facultad_obj.universidad_id):
            raise ValueError("Universidad no existe")

        facultad = FacultadRepository.create(facultad_obj)
        
        cache = current_app.extensions.get('cache')
        if cache:
            cache.delete('facultad:all')
        
        return facultad

    @staticmethod
    def actualizar_facultad(fid: int, facultad_obj):
        existente = FacultadRepository.get_by_id(fid)
        if not existente:
            return None

        # Actualizar campos
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

        facultad = FacultadRepository.update(existente)
        
        cache = current_app.extensions.get('cache')
        if cache:
            cache.set(f'facultad:{fid}', facultad, timeout=60)
            cache.delete('facultad:all')
        
        return facultad

    @staticmethod
    def eliminar_facultad(fid: int):
        existente = FacultadRepository.get_by_id(fid)
        if not existente:
            return None

        FacultadRepository.delete(existente)
        
        cache = current_app.extensions.get('cache')
        if cache:
            cache.delete(f'facultad:{fid}')
            cache.delete('facultad:all')
        
        return existente