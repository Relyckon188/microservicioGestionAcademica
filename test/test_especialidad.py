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
