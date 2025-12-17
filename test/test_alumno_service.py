import pytest
from app.services.alumno_service import AlumnoService
from app.exceptions import DuplicateDNIException

def test_crear_alumno_dni_duplicado(mocker):
    repo = mocker.Mock()
    repo.get_by_dni.return_value = {"dni": "12345678"}

    service = AlumnoService(repo)

    with pytest.raises(DuplicateDNIException):
        service.crear_alumno({"dni": "12345678", "nombre": "Ana"})

#TDD: test primero
#DIP: repo mockeado
#KISS: test simple y claro