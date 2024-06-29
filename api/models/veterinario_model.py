from sqlalchemy import Column, ForeignKey, Integer, String


from models.pessoa_model import Pessoa

class Veterinario(Pessoa):
    __tablename__ = 'veterinarios'
    id = Column(Integer, ForeignKey('pessoa.id'), primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def to_dict(self):
        dict_pessoa = super().to_dict()
        dict_pessoa['nome'] = self.nome
        dict_pessoa['cpf'] = self.cpf
        dict_pessoa['telefone'] = self.telefone
        dict_pessoa['email'] = self.email
        return dict_pessoa