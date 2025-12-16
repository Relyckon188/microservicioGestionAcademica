from app.repositories.universidad_repository import UniversidadRepository
from flask import current_app

class UniversidadService:

    @staticmethod
    def obtener_todas():
        # Verificar si cache está configurado
        cache = current_app.config.get('CACHE_TYPE', None)
        if cache and cache != 'NullCache':
            cached = current_app.extensions['cache'].get('universidad:all')
            if cached:
                return cached
        
        universidades = UniversidadRepository.get_all()
        
        if cache and cache != 'NullCache':
            current_app.extensions['cache'].set('universidad:all', universidades, timeout=60)
        
        return universidades

    @staticmethod
    def obtener_por_id(uid: int):
        cache = current_app.extensions.get('cache')
        
        if cache:
            cached = cache.get(f'universidad:{uid}')
            if cached:
                return cached
        
        universidad = UniversidadRepository.get_by_id(uid)
        
        if cache:
            cache.set(f'universidad:{uid}', universidad, timeout=60)
        
        return universidad

    @staticmethod
    def crear_universidad(data):
        universidad = UniversidadRepository.create(data)
        
        cache = current_app.extensions.get('cache')
        if cache:
            cache.delete('universidad:all')
        
        return universidad

    @staticmethod
    def actualizar_universidad(uid: int, data):
        obj = UniversidadRepository.get_by_id(uid)
        if not obj:
            return None
        
        universidad = UniversidadRepository.update(obj, data)
        
        cache = current_app.extensions.get('cache')
        if cache:
            cache.set(f'universidad:{uid}', universidad, timeout=60)
            cache.delete('universidad:all')
        
        return universidad

    @staticmethod
    def eliminar_universidad(uid: int):
        obj = UniversidadRepository.get_by_id(uid)
        if not obj:
            return None
        
        UniversidadRepository.delete(obj)
        
        cache = current_app.extensions.get('cache')
        if cache:
            cache.delete(f'universidad:{uid}')
            cache.delete('universidad:all')
        
        return obj