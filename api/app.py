from flask import Flask
from config import Config
from extensions import db,ma
import controllers
from models.base_model import Base
from models.pessoa_model import Pessoa
from models.tutor_model import Tutor
from models.veterinario_model import Veterinario
from models.estagiario_model import Estagiario
from models.animal_model import Animal
from models.consulta_model import Consulta



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    

    app.register_blueprint(controllers.tutor_bp, url_prefix='/tutores' )
    app.register_blueprint(controllers.veterinario_bp, url_prefix='/veterinarios' )
    app.register_blueprint(controllers.consulta_bp, url_prefix='/consultas' )
    app.register_blueprint(controllers.animal_bp, url_prefix='/animais' )
    app.register_blueprint(controllers.estagiario_bp, url_prefix='/estagiarios')

    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True)