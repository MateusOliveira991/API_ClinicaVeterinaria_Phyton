# VeterinarioRepository.py
from extensions import db
from api.models.veterinario_model import Veterinario

class VeterinarioRepository:

    @staticmethod
    def get_all():
        return db.session.query(Veterinario).all()

    @staticmethod
    def get_by_id(id):
        return db.session.query(Veterinario).filter(Veterinario.id == id).first()

    @staticmethod
    def create(veterinario):
        db.session.add(veterinario)
        db.session.commit()
        return veterinario

    @staticmethod
    def update(veterinario):
        db.session.commit()
        return veterinario

    @staticmethod
    def delete(veterinario):
        db.session.delete(veterinario)
        db.session.commit()