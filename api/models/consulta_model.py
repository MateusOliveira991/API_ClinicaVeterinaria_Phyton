from sqlalchemy import Column, Integer, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from extensions import db

class Consulta(db.Model):
  
    __tablename__ = 'consultas'
    
    id = Column(Integer, primary_key=True)
    id_animal = Column(Integer, ForeignKey('animais.id'), nullable=False)
    id_veterinario = Column(Integer, ForeignKey('veterinarios.id'), 
    nullable=False)
    id_estagiario = Column(Integer, ForeignKey('estagiarios.id'), nullable=True)
  
    data = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    
    animal = relationship("Animal", backref="consultas")
    veterinario = relationship("Veterinario", backref="consultas")
    estagiario = relationship("Estagiario", backref="consultas", foreign_keys=[id_estagiario])
   

    def to_dict(self):
        return {
            'id': self.id,
            'id_animal': self.id_animal,
            'id_veterinario': self.id_veterinario,
            'id_estagiario': self.id_estagiario,
            'data': self.data.isoformat() if self.data else None,
            'hora': str(self.hora) if self.hora else None,
            'animal': self.animal.to_dict() if self.animal else None,
            'veterinario': self.veterinario.to_dict() if self.veterinario else 
            None,
            'estagiario': self.estagiario.to_dict() if self.estagiario else None,
            
        }