# app/common/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from Admin.schemas import RegisterSchema, LoginSchema
from Admin.services import auth_service

auth_bp = Blueprint("auth", __name__)

# Register user (doctor/member only, admin cannot self-register)
@auth_bp.route("/register", methods=["POST"])
def register():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"msg": "Missing JSON payload"}), 400

    schema = RegisterSchema()
    errors = schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    username = payload["username"]
    email = payload["email"]
    password = payload["password"]
    role = payload["role"]

    if role == "admin":
        return jsonify({"msg": "Cannot self-register as admin"}), 403

    try:
        user = auth_service.register_user(username, email, password, role)
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

    claims = {"role": user.role, "username": user.username}
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({
        "access_token": access_token,
        "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
    }), 201


# Login user (any role)
@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"msg": "Missing JSON payload"}), 400

    schema = LoginSchema()
    errors = schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    user = auth_service.authenticate(payload["username"], payload["password"])
    if not user:
        return jsonify({"msg": "Invalid username or password"}), 401

    claims = {"role": user.role, "username": user.username}
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({
        "access_token": access_token,
        "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
    }), 200


# Logout user (JWT is stateless → client just discards token)
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"msg": "Logged out successfully"}), 200
