from flask import Blueprint, request, jsonify
from extensions import db
from services.consulta_service import ConsultaService
from utils.exceptions import ValidationError, NotFoundError

consulta_bp = Blueprint("consulta", __name__)
consulta_service = ConsultaService(db.session)

@consulta_bp.route("/consultas", methods=["POST"])
def create_consulta():
    try:
        data = request.get_json()
        consulta = consulta_service.create(data)
        return jsonify(consulta.to_dict()), 201
    except ValidationError as e:
        return jsonify(e.to_dict()), 400

@consulta_bp.route("/consultas/<int:id>", methods=["GET"])
def get_consulta(id):
    try:
        consulta = consulta_service.get(id)
        if not consulta:
            raise NotFoundError("Consulta não encontrada.")
        return jsonify(consulta.to_dict())
    except NotFoundError as e:
        return jsonify(e.to_dict()), 404

@consulta_bp.route("/consultas", methods=["GET"])
def get_all_consultas():
    consultas = consulta_service.get_all()
    return jsonify([consulta.to_dict() for consulta in consultas])

@consulta_bp.route("/consultas/<int:id>", methods=["PUT"])
def update_consulta(id):
    try:
        data = request.get_json()
        consulta = consulta_service.get(id)
        if not consulta:
            raise NotFoundError("Consulta não encontrada.")
        consulta_service.update(consulta, data)
        return jsonify(consulta.to_dict())
    except ValidationError as e:
        return jsonify(e.to_dict()), 400
    except NotFoundError as e:
        return jsonify(e.to_dict()), 404

@consulta_bp.route("/consultas/<int:id>", methods=["DELETE"])
def delete_consulta(id):
    try:
        consulta = consulta_service.get(id)
        if not consulta:
            raise NotFoundError("Consulta não encontrada.")
        consulta_service.delete(consulta)
        return '', 204
    except NotFoundError as e:
        return jsonify(e.to_dict()), 404

@consulta_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 400
    return response

@consulta_bp.errorhandler(NotFoundError)
def handle_not_found_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 404
    return response
