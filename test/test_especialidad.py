from app.models.especialidad import Especialidad
from app.models.facultad import Facultad
from app.services.especialidad_service import EspecialidadService
from app.services.facultad_service import FacultadService
from app.services.universidad_service import UniversidadService

def nueva_especialidad(fid):
    return Especialidad(
        nombre="Matematicas",
        letra="A",
        observacion="Observacion de prueba",
        facultad_id=fid
    )

def test_crear_especialidad(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = FacultadService.crear_facultad(
        Facultad(nombre="FC", abreviatura="FC", directorio="/d", sigla="FC",
                 email="a@a.com", universidad_id=u.id)
    )
    e = nueva_especialidad(f.id)
    EspecialidadService.crear_especialidad(e)
    assert e.id is not None
    assert e.nombre == "Matematicas"

def test_obtener_especialidad_por_id(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = FacultadService.crear_facultad(
        Facultad(nombre="FC", abreviatura="FC", directorio="/d", sigla="FC",
                 email="a@a.com", universidad_id=u.id)
    )
    e = nueva_especialidad(f.id)
    EspecialidadService.crear_especialidad(e)
    r = EspecialidadService.obtener_por_id(e.id)
    assert r.id == e.id
    assert r.nombre == "Matematicas"

def test_obtener_todas_especialidades(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = FacultadService.crear_facultad(
        Facultad(nombre="FC", abreviatura="FC", directorio="/d", sigla="FC",
                 email="a@a.com", universidad_id=u.id)
    )
    e1 = nueva_especialidad(f.id)
    e2 = nueva_especialidad(f.id)
    EspecialidadService.crear_especialidad(e1)
    EspecialidadService.crear_especialidad(e2)
    lista = EspecialidadService.obtener_todas()
    assert len(lista) == 2

def test_actualizar_especialidad(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = FacultadService.crear_facultad(
        Facultad(nombre="FC", abreviatura="FC", directorio="/d", sigla="FC",
                 email="a@a.com", universidad_id=u.id)
    )
    e = nueva_especialidad(f.id)
    EspecialidadService.crear_especialidad(e)
    data = Especialidad(nombre="Actualizada", letra="B", observacion="Cambio", facultad_id=f.id)
    updated = EspecialidadService.actualizar_especialidad(e.id, data)
    assert updated.nombre == "Actualizada"
    assert updated.letra == "B"

def test_eliminar_especialidad(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = FacultadService.crear_facultad(
        Facultad(nombre="FC", abreviatura="FC", directorio="/d", sigla="FC",
                 email="a@a.com", universidad_id=u.id)
    )
    e = nueva_especialidad(f.id)
    EspecialidadService.crear_especialidad(e)
    EspecialidadService.eliminar_especialidad(e.id)
    assert EspecialidadService.obtener_por_id(e.id) is None
