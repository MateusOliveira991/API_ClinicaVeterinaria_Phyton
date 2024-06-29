from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from extensions import db
class Animal(db.Model):
    __tablename__ = 'animais'
    
    id = Column(Integer, primary_key=True)
    id_tutor = Column(Integer, ForeignKey('tutores.id'), nullable=False)
    nome = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    raca = Column(String, nullable=False)
    sexo = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    descricao = Column(String, nullable=False)
  
    tutor = relationship("Tutor", backref="animais")

    def to_dict(self):
        return {
            'id': self.id,
            'id_tutor': self.id_tutor,
            'nome': self.nome,
            'especie': self.especie,
            'raca': self.raca,
            'sexo': self.sexo,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'descricao': self.descricao,
            }
        