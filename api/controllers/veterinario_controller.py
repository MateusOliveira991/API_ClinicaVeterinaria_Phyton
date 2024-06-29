from flask import Blueprint, request, jsonify
from extensions import db
from services.veterinario_service import VeterinarioService
from utils.exceptions import ValidationError, NotFoundError

veterinario_bp = Blueprint("veterinario", __name__)
veterinario_service = VeterinarioService(db.session)


@veterinario_bp.route("/veterinarios", methods=["POST"])
def create_veterinario():
    try:
        data = request.get_json()
        veterinario = veterinario_service.create(data)
        return jsonify(veterinario.to_dict()), 201
    except ValidationError as e:
        return jsonify(e.to_dict()), 400


@veterinario_bp.route("/veterinarios/<int:id>", methods=["GET"])
def get_veterinario(id):
    veterinario = veterinario_service.get(id)
    if not veterinario:
        raise NotFoundError("Médico não encontrado.")
    return jsonify(veterinario.to_dict())


@veterinario_bp.route("/veterinarios", methods=["GET"])
def get_all_veterinarios():
    veterinarios = veterinario_service.get_all()
    return jsonify([veterinario.to_dict() for veterinario in veterinarios])


@veterinario_bp.route("/veterinarios/<int:id>", methods=["PUT"])
def update_veterinario(id):
    try:
        data = request.get_json()
        veterinario = veterinario_service.get(id)
        if not veterinario:
            raise NotFoundError("Médico não encontrado.")
        veterinario_service.update(veterinario, data)
        return jsonify(veterinario.to_dict())
    except ValidationError as e:
        return jsonify(e.to_dict()), 400


@veterinario_bp.route("/veterinarios/<int:id>", methods=["DELETE"])
def delete_veterinario(id):
    veterinario = veterinario_service.get(id)
    if not veterinario:
        raise NotFoundError("Médico não encontrado.")
    veterinario_service.delete(veterinario)
    return "", 204


@veterinario_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 400
    return response


@veterinario_bp.errorhandler(NotFoundError)
def handle_not_found_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 404
    return response