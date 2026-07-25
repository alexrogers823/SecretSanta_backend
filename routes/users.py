from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from models import User, db

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("", methods=["GET"])
def list_users():
    query = User.query
    name = request.args.get("name")
    email = request.args.get("email")

    if name:
        query = query.filter_by(name=name)
    if email:
        query = query.filter_by(email=email)

    return jsonify([user.to_dict() for user in query.all()])


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@users_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    user = User(name=name, email=email)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "a user with that email already exists"}), 409

    return jsonify(user.to_dict()), 201


@users_bp.route("/<int:user_id>", methods=["PUT"])
def replace_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    user.name = name
    user.email = email
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "a user with that email already exists"}), 409

    return jsonify(user.to_dict())


@users_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json(silent=True) or {}

    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "a user with that email already exists"}), 409

    return jsonify(user.to_dict())


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204
