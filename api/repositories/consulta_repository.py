# ConsultaRepository.py
from extensions import db
from models.consulta_model import Consulta

class ConsultaRepository:

    @staticmethod
    def get_all():
        return db.session.query(Consulta).all()

    @staticmethod
    def get_by_id(id):
        return db.session.query(Consulta).filter(Consulta.id == id).first()

    @staticmethod
    def create(consulta):
        db.session.add(consulta)
        db.session.commit()
        return consulta

    @staticmethod
    def update(consulta):
        db.session.commit()
        return consulta

    @staticmethod
    def delete(consulta):
        db.session.delete(consulta)
        db.session.commit()