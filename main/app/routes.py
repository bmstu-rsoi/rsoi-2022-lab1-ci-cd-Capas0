from flask import Blueprint, jsonify, request, url_for
from marshmallow import ValidationError
from sqlalchemy.exc import DataError

from .extention import db
from .models import Person
from .schemas import PersonSchema

api = Blueprint('api', __name__)

person_serializer = PersonSchema()


@api.route('/persons', methods=['GET'])
def list_persons():
    persons = Person.query.all()
    return jsonify(person_serializer.dump(persons, many=True)), 200


@api.route('/persons', methods=['POST'])
def create_person():
    try:
        person = person_serializer.load(request.json)
        db.session.add(person)
        db.session.commit()
        return '', 201, {'Location': url_for('api.get_person', person_id=person.id)}
    except ValidationError as err:
        return jsonify({
            'message': 'Invalid data',
            'errors': err.messages
        }), 400


@api.route('/persons/<person_id>', methods=['GET'])
def get_person(person_id):
    try:
        person = Person.query.get(person_id)
    except DataError:
        person = None

    if person is None:
        return jsonify({'message': f"Not found Person for ID '{person_id}'"}), 404
    return jsonify(person_serializer.dump(person)), 200


@api.route('/persons/<person_id>', methods=['DELETE'])
def delete_person(person_id):
    try:
        person = Person.query.get(person_id)
    except DataError:
        person = None

    if person is not None:
        db.session.delete(person)
        db.session.commit()
    return '', 204


@api.route('/persons/<person_id>', methods=['PATCH'])
def edit_person(person_id):
    try:
        person = Person.query.get(person_id)
    except DataError:
        person = None
    if person is None:
        return jsonify({'message': f"Not found Person for ID '{person_id}'"}), 404

    try:
        person_serializer.load(request.json)
    except ValidationError as err:
        return jsonify({
            'message': 'Invalid data',
            'errors': err.messages
        }), 400

    for key, value in request.json.items():
        setattr(person, key, value)
    db.session.commit()
    return jsonify(person_serializer.dump(person)), 200
