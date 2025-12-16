from app.repositories.especialidad_repository import EspecialidadRepository
from app.repositories.facultad_repository import FacultadRepository
from flask import current_app

class EspecialidadService:

    @staticmethod
    def obtener_todas():
        cache = current_app.extensions.get('cache')
        
        if cache:
            cached = cache.get("especialidad_all")
            if cached:
                return cached
        
        especialidades = EspecialidadRepository.get_all()
        
        if cache:
            cache.set("especialidad_all", especialidades, timeout=60)
        
        return especialidades

    @staticmethod
    def obtener_por_id(eid: int):
        cache = current_app.extensions.get('cache')
        
        if cache:
            cache_key = f"especialidad_{eid}"
            cached = cache.get(cache_key)
            if cached:
                return cached
        
        especialidad = EspecialidadRepository.get_by_id(eid)
        
        if cache and especialidad:
            cache.set(f"especialidad_{eid}", especialidad, timeout=60)
        
        return especialidad

    @staticmethod
    def crear_especialidad(data):
        if not FacultadRepository.get_by_id(data.facultad_id):
            raise ValueError("La facultad no existe")

        especialidad = EspecialidadRepository.create(data)
        
        cache = current_app.extensions.get('cache')
        if cache:
            cache.delete("especialidad_all")
        
        return especialidad

    @staticmethod
    def actualizar_especialidad(eid: int, data):
        obj = EspecialidadRepository.get_by_id(eid)
        if not obj:
            return None
        
        especialidad = EspecialidadRepository.update(obj, data)
        
        cache = current_app.extensions.get('cache')
        if cache:
            cache.set(f"especialidad_{eid}", especialidad, timeout=60)
            cache.delete("especialidad_all")
        
        return especialidad

    @staticmethod
    def eliminar_especialidad(eid: int):
        obj = EspecialidadRepository.get_by_id(eid)
        if not obj:
            return None
        
        EspecialidadRepository.delete(obj)
        
        cache = current_app.extensions.get('cache')
        if cache:
            cache.delete(f"especialidad_{eid}")
            cache.delete("especialidad_all")
        
        return obj