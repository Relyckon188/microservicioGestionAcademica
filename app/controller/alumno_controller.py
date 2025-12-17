from app.services.alumno_service import AlumnoService
from app.repositories.alumno_repository import AlumnoRepository

class AlumnoController:

    @staticmethod
    def crear(data):
        service = AlumnoService(AlumnoRepository())
        alumno = service.crear_alumno(data)
        return alumno, 201
