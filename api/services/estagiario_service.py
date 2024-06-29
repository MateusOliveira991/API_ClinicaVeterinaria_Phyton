from services.pessoa_service import PessoaService
from models.estagiario_model import Estagiario

class EstagiarioService(PessoaService):
    def __init__(self, session):
        super().__init__(Estagiario, session)
