from dataclasses import dataclass
from app import db

@dataclass
class Especialidad(db.Model):
    __tablename__ = 'especialidades'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    letra: str = db.Column(db.String(1), nullable=False)
    observacion: str = db.Column(db.String(255), nullable=True)

    # FK a Facultad
    facultad_id = db.Column(db.Integer, db.ForeignKey("facultades.id"), nullable=False)

    # Relaciones
    facultad = db.relationship("Facultad", back_populates="especialidades")
