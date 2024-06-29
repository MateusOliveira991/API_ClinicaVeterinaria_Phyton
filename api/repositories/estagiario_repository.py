# EstagiarioRepository.py
from extensions import db
from api.models.estagiario_model import Estagiario

class EstagiarioRepository:

    @staticmethod
    def get_all():
        return db.session.query(Estagiario).all()

    @staticmethod
    def get_by_id(id):
        return db.session.query(Estagiario).filter(Estagiario.id == id).first()

    @staticmethod
    def create(estagiario):
        db.session.add(estagiario)
        db.session.commit()
        return estagiario

    @staticmethod
    def update(estagiario):
        db.session.commit()
        return estagiario

    @staticmethod
    def delete(estagiario):
        db.session.delete(estagiario)
        db.session.commit()