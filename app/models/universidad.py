from dataclasses import dataclass
from app import db

@dataclass
class Universidad(db.Model):
    __tablename__ = "universidades"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    sigla: str = db.Column(db.String(10), nullable=False)

    # Relaciones
    facultades = db.relationship("Facultad", back_populates="universidad", lazy=True)
