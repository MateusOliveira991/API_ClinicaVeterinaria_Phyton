from services.pessoa_service import PessoaService
from models.tutor_model import Tutor
from utils.validators import validate_cpf, validate_email, validate_phone
from utils.exceptions import ValidationError

class TutorService(PessoaService):
    def __init__(self, session):
        super().__init__(Tutor, session)

    