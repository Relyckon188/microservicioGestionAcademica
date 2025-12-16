from dataclasses import dataclass, asdict
from app import db

@dataclass
class Especialidad(db.Model):
    __tablename__ = 'especialidades'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    letra: str = db.Column(db.String(1), nullable=False)
    observacion: str = db.Column(db.String(255), nullable=True)
    facultad_id = db.Column(db.Integer, db.ForeignKey("facultades.id"), nullable=False)

    # Relaciones
    facultad = db.relationship("Facultad", back_populates="especialidades")
    
    def to_dict_completo(self):
        """Devuelve un diccionario con todas las relaciones necesarias"""
        data = {
            "id": self.id,
            "nombre": self.nombre,
            "letra": self.letra,
            "observacion": self.observacion,
            "facultad_id": self.facultad_id
        }
        
        # Verificar si la relación está cargada
        if self.facultad:
            data["facultad_nombre"] = self.facultad.nombre
            
            # Verificar si universidad está cargada
            if hasattr(self.facultad, 'universidad') and self.facultad.universidad:
                data["universidad_nombre"] = self.facultad.universidad.nombre
                
        return data
    
    def to_dict_simple(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "letra": self.letra,
            "observacion": self.observacion,
            "facultad_id": self.facultad_id
        }