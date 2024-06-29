from services.base_service import BaseService
from models.consulta_model import Consulta

class ConsultaService(BaseService):
    def __init__(self, session):
        super().__init__(Consulta, session)
