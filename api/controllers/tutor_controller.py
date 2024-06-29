from flask import Blueprint, request, jsonify
from extensions import db
from services.tutor_service import TutorService
from utils.exceptions import ValidationError, NotFoundError

tutor_bp = Blueprint("tutor", __name__)
tutor_service = TutorService(db.session)

@tutor_bp.route("/tutores", methods=["POST"])
def create_tutor():
    try:
        data = request.get_json()
        tutor = tutor_service.create(data)
        return jsonify(tutor.to_dict()), 201
    except ValidationError as e:
        return jsonify(e.to_dict()), 400

@tutor_bp.route("/tutores/<int:id>", methods=["GET"])
def get_tutor(id):
    try:
        tutor = tutor_service.get(id)
        if not tutor:
            raise NotFoundError("Tutor não encontrado.")
        return jsonify(tutor.to_dict())
    except NotFoundError as e:
        return jsonify(e.to_dict()), 404

@tutor_bp.route("/tutores", methods=["GET"])
def get_all_tutores():
    tutores = tutor_service.get_all()
    return jsonify([tutor.to_dict() for tutor in tutores])

@tutor_bp.route("/tutores/<int:id>", methods=["PUT"])
def update_tutor(id):
    try:
        data = request.get_json()
        tutor = tutor_service.get(id)
        if not tutor:
            raise NotFoundError("Tutor não encontrado.")
        tutor_service.update(tutor, data)
        return jsonify(tutor.to_dict())
    except ValidationError as e:
        return jsonify(e.to_dict()), 400
    except NotFoundError as e:
        return jsonify(e.to_dict()), 404

@tutor_bp.route("/tutores/<int:id>", methods=["DELETE"])
def delete_tutor(id):
    try:
        tutor = tutor_service.get(id)
        if not tutor:
            raise NotFoundError("Tutor não encontrado.")
        tutor_service.delete(tutor)
        return '', 204
    except NotFoundError as e:
        return jsonify(e.to_dict()), 404

@tutor_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 400
    return response

@tutor_bp.errorhandler(NotFoundError)
def handle_not_found_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 404
    return response
