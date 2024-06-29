from services.base_service import BaseService
from models.animal_model import Animal

class AnimalService(BaseService):
    def __init__(self, session):
        super().__init__(Animal, session)
