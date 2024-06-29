from extensions import db
from api.models.animal_model import Animal

class AnimalRepository:

    @staticmethod
    def get_all():
        return db.session.query(Animal).all()

    @staticmethod
    def get_by_id(id):
        return db.session.query(Animal).filter(Animal.id == id).first()

    @staticmethod
    def create(animal):
        db.session.add(animal)
        db.session.commit()
        return animal

    @staticmethod
    def update(animal):
        db.session.commit()
        return animal

    @staticmethod
    def delete(animal):
        db.session.delete(animal)
        db.session.commit()