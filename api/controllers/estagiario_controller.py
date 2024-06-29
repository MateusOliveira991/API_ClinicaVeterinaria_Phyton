from flask import Blueprint, request, jsonify
from extensions import db
from services.estagiario_service import EstagiarioService
from utils.exceptions import ValidationError, NotFoundError

estagiario_bp = Blueprint('estagiario', __name__)
estagiario_service = EstagiarioService(db.session)

@estagiario_bp.route('/estagiarios', methods=['POST'])
def create_estagiario():
    try:
        data = request.get_json()
        estagiario = estagiario_service.create(data)
        return jsonify(estagiario.to_dict()), 201
    except ValidationError as e:
        return jsonify(e.to_dict()), 400

@estagiario_bp.route('/estagiarios/<int:id>', methods=['GET'])
def get_estagiario(id):
    try:
        estagiario = estagiario_service.get(id)
        if not estagiario:
            raise NotFoundError("Estagiário não encontrado.")
        return jsonify(estagiario.to_dict())
    except NotFoundError as e:
        return jsonify(e.to_dict()), 404

@estagiario_bp.route('/estagiarios', methods=['GET'])
def get_all_estagiarios():
    estagiarios = estagiario_service.get_all()
    return jsonify([estagiario.to_dict() for estagiario in estagiarios])

@estagiario_bp.route('/estagiarios/<int:id>', methods=['PUT'])
def update_estagiario(id):
    try:
        data = request.get_json()
        estagiario = estagiario_service.get(id)
        if not estagiario:
            raise NotFoundError("Estagiário não encontrado.")
        estagiario_service.update(estagiario, data)
        return jsonify(estagiario.to_dict())
    except ValidationError as e:
        return jsonify(e.to_dict()), 400
    except NotFoundError as e:
        return jsonify(e.to_dict()), 404

@estagiario_bp.route('/estagiarios/<int:id>', methods=['DELETE'])
def delete_estagiario(id):
    try:
        estagiario = estagiario_service.get(id)
        if not estagiario:
            raise NotFoundError("Estagiário não encontrado.")
        estagiario_service.delete(estagiario)
        return '', 204
    except NotFoundError as e:
        return jsonify(e.to_dict()), 404

@estagiario_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 400
    return response

@estagiario_bp.errorhandler(NotFoundError)
def handle_not_found_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 404
    return response
