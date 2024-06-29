from services.base_service import BaseService
from models.pessoa_model import Pessoa
from utils.validators import validate_cpf, validate_email, validate_phone, validate_nome

class PessoaService(BaseService):
    def __init__(self,model, session):
        super().__init__(model, session)

    def create(self, data):
        data['cpf'] = validate_cpf(data.get('cpf', ''))
        data['email'] = validate_email(data.get('email', ''))
        data['telefone'] = validate_phone(data.get('telefone', ''))
        data['nome'] = validate_nome(data.get('nome', ''))
        return super().create(data)

    def update(self, instance, data):
        if 'cpf' in data:
            data['cpf'] = validate_cpf(data['cpf'])
        if 'email' in data:
            data['email'] = validate_email(data['email'])
        if 'telefone' in data:
            data['telefone'] = validate_phone(data['telefone'])
        if 'nome' in data:
            data['nome'] = validate_nome(data['nome'])
        return super().update(instance, data)