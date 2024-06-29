from flask import Flask
from controllers.tutor_controller import tutor_bp
from controllers.veterinario_controller import veterinario_bp
from controllers.consulta_controller import consulta_bp
from controllers.animal_controller import animal_bp
from controllers.estagiario_controller import estagiario_bp

#Pra rodar: cd api e python app.py


def register_routes(app: Flask):
    app.register_blueprint(tutor_bp, url_prefix="/api")
    app.register_blueprint(veterinario_bp, url_prefix="/api")
    app.register_blueprint(consulta_bp, url_prefix="/api")
    app.register_blueprint(animal_bp, url_prefix="/api")
    app.register_blueprint(estagiario_bp, url_prefix="/api")
