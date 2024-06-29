from services.pessoa_service import PessoaService
from services.base_service import BaseService
from models.veterinario_model import Veterinario


class VeterinarioService(PessoaService):
    def __init__(self, session):
        super().__init__(Veterinario, session)
