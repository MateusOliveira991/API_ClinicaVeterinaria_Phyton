from flask import Blueprint, request, jsonify
from extensions import db
from services.animal_service import AnimalService
from utils.exceptions import ValidationError, NotFoundError

animal_bp = Blueprint('animal', __name__)
animal_service = AnimalService(db.session)

@animal_bp.route('/animais', methods=['POST'])
def create_animal():
    try:
        data = request.get_json()
        animal = animal_service.create(data)
        return jsonify(animal.to_dict()), 201
    except ValidationError as e:
        return jsonify(e.to_dict()), 400

@animal_bp.route('/animais/<int:id>', methods=['GET'])
def get_animal(id):
    animal = animal_service.get(id)
    if not animal:
        raise NotFoundError("Animal não encontrado.")
    return jsonify(animal.to_dict())

@animal_bp.route('/animais', methods=['GET'])
def get_all_animais():
    try:
        animais = animal_service.get_all()
        animais_list = [animal.to_dict() for animal in animais]
        return jsonify(animais_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@animal_bp.route('/animais/<int:id>', methods=['PUT'])
def update_animal(id):
    try:
        data = request.get_json()
        animal = animal_service.get(id)
        if not animal:
            raise NotFoundError("Animal não encontrado.")
        animal_service.update(animal, data)
        return jsonify(animal.to_dict())
    except ValidationError as e:
        return jsonify(e.to_dict()), 400

@animal_bp.route('/animais/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animal = animal_service.get(id)
    if not animal:
        raise NotFoundError("Animal não encontrado.")
    animal_service.delete(animal)
    return '', 204

@animal_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 400
    return response

@animal_bp.errorhandler(NotFoundError)
def handle_not_found_error(error):
    response = jsonify(error.to_dict())
    response.status_code = 404
    return response
