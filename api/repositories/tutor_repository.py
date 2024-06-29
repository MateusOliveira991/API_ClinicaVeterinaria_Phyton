# TutorRepository.py
from extensions import db
from models.tutor_model import Tutor

class TutorRepository:

    @staticmethod
    def get_all():
        return db.session.query(Tutor).all()

    @staticmethod
    def get_by_id(id):
        return db.session.query(Tutor).filter(Tutor.id == id).first()

    @staticmethod
    def create(tutor):
        db.session.add(tutor)
        db.session.commit()
        return tutor

    @staticmethod
    def update(tutor):
        db.session.commit()
        return tutor

    @staticmethod
    def delete(tutor):
        db.session.delete(tutor)
        db.session.commit()