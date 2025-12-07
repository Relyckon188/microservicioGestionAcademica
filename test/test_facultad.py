from app.models.facultad import Facultad
from app.services.facultad_service import FacultadService
from app.services.universidad_service import UniversidadService

def base_facultad(uid):         #cargar datos
    return Facultad(
        nombre="Facultad de Ciencias",
        abreviatura="FCC",
        directorio="/facultad/ciencias",
        sigla="FC",
        codigopostal="12345",
        ciudad="Ciudad",
        domicilio="Calle 123",
        telefono="123456789",
        contacto="Juan Perez",
        email="1234@gmail.com",
        universidad_id=uid
    )

def test_crear_facultad(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = base_facultad(u.id)
    FacultadService.crear_facultad(f)
    assert f.id is not None
    assert f.nombre == "Facultad de Ciencias"

def test_obtener_facultad_por_id(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = FacultadService.crear_facultad(base_facultad(u.id))
    r = FacultadService.obtener_por_id(f.id)
    assert r.id == f.id
    assert r.nombre == f.nombre

def test_obtener_todas_facultades(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f1 = FacultadService.crear_facultad(base_facultad(u.id))
    f2 = FacultadService.crear_facultad(base_facultad(u.id))
    lista = FacultadService.obtener_todas()
    assert len(lista) == 2

def test_actualizar_facultad(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = FacultadService.crear_facultad(base_facultad(u.id))
    actualizado = Facultad(
        nombre="Nueva",
        abreviatura="NN",
        directorio="/d",
        sigla="N",
        codigopostal="9999",
        ciudad="X",
        domicilio="Y",
        telefono="0",
        contacto="A",
        email="b@b.com",
        universidad_id=u.id
    )
    updated = FacultadService.actualizar_facultad(f.id, actualizado)
    assert updated.nombre == "Nueva"
    assert updated.abreviatura == "NN"

def test_eliminar_facultad(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = FacultadService.crear_facultad(base_facultad(u.id))
    FacultadService.eliminar_facultad(f.id)
    assert FacultadService.obtener_por_id(f.id) is None
