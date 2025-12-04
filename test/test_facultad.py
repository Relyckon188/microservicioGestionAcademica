from app.models.facultad import Facultad
from app.services.facultad_service import FacultadService
from app.services.universidad_service import UniversidadService

def base_facultad(universidad_id):
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
        universidad_id=universidad_id
    )

def test_crear_facultad(app):
    u = UniversidadService.crear_universidad({"nombre": "UNA", "sigla": "UN"})
    f = base_facultad(u.id)

    FacultadService.crear_facultad(f)

    assert f.id is not None
    assert f.nombre == "Facultad de Ciencias"
