from models.pessoa_model import Pessoa
from utils.validators import validate_date, validate_endereco
from sqlalchemy import Column, ForeignKey, Integer, String


class Tutor(Pessoa):
    __tablename__ = 'tutores'
    id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    data_nascimento = Column(String, nullable=False)

    def to_dict(self):
        dict_pessoa = super().to_dict()
        dict_pessoa['nome'] = self.nome
        dict_pessoa['cpf'] = self.cpf
        dict_pessoa['telefone'] = self.telefone
        dict_pessoa['email'] = self.email
        dict_pessoa['endereco'] = self.endereco
        dict_pessoa['data_nascimento'] = self.data_nascimento
        return dict_pessoa