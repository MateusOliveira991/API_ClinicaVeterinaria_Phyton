
#Os serviços são responsáveis por implementar a lógica de negócios da aplicação. Eles coordenam as operações entre os modelos e os repositórios, aplicando regras de negócios e garantindo a consistência dos dados. Os serviços geralmente contêm a lógica para manipular os dados, realizar validações, executar cálculos e realizar outras tarefas relacionadas à funcionalidade específica da aplicação.



class BaseService:
    def __init__(self, model, session):
        self.model = model
        self.session = session
    
    def create(self, data):
        instance = self.model(**data)
        self.session.add(instance)
        self.session.commit()
        return instance
    
    def update(self, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)
        self.session.commit()
        return instance
    
    def delete(self, instance):
        self.session.delete(instance)
        self.session.commit()
    
    def get(self, id):
        return self.session.query(self.model).get(id)
    
    def get_all(self):
        return self.session.query(self.model).all()
