from dataclasses import dataclass
from app import db

@dataclass
class Facultad(db.Model):
    __tablename__ = 'facultades'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    abreviatura: str = db.Column(db.String(10), nullable=False)
    directorio: str = db.Column(db.String(100), nullable=False)
    sigla: str = db.Column(db.String(10), nullable=False)
    email: str = db.Column(db.String(100), nullable=False)
    #opcional
    codigopostal: str = db.Column(db.String(10), nullable=True)
    ciudad: str = db.Column(db.String(50), nullable=True)
    domicilio: str = db.Column(db.String(100), nullable=True)
    telefono: str = db.Column(db.String(20), nullable=True)
    contacto: str = db.Column(db.String(100), nullable=True)

    # FK a Universidad
    universidad_id = db.Column(db.Integer, db.ForeignKey("universidades.id"), nullable=False)

    # Relaciones
    universidad = db.relationship("Universidad", back_populates="facultades")
    especialidades = db.relationship("Especialidad", back_populates="facultad", lazy=True)
