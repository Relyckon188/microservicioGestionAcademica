from app.models.universidad import Universidad
from app.services.universidad_service import UniversidadService

def nueva_universidad():
    return {"nombre": "Universidad Nacional", "sigla": "UN"}    #diccionario

def test_universidad_creation(app):
    data = nueva_universidad()
    u = Universidad(**data)             #instancia
    assert u.nombre == "Universidad Nacional"           #verificar que quede en instancia
    assert u.sigla == "UN"

def test_crear_universidad(app):
    data = nueva_universidad()
    u = UniversidadService.crear_universidad(data)
    assert u.id is not None             #verifica que db le asignó id
    assert u.nombre == "Universidad Nacional"

def test_universidad_busqueda(app):
    data = nueva_universidad()
    u = UniversidadService.crear_universidad(data)
    r = UniversidadService.obtener_por_id(u.id)
    assert r.nombre == "Universidad Nacional"

def test_buscar_universidades(app):
    u1 = UniversidadService.crear_universidad(nueva_universidad())
    u2 = UniversidadService.crear_universidad(nueva_universidad())
    universidades = UniversidadService.obtener_todas()
    assert len(universidades) == 2

def test_actualizar_universidad(app):
    u = UniversidadService.crear_universidad(nueva_universidad())
    updated = UniversidadService.actualizar_universidad(u.id, {"nombre": "Actualizada"})
    assert updated.nombre == "Actualizada"          #verificar la actualizacion

def test_borrar_universidad(app):
    u = UniversidadService.crear_universidad(nueva_universidad())
    UniversidadService.eliminar_universidad(u.id)
    assert UniversidadService.obtener_por_id(u.id) is None
