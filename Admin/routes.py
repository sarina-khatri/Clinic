# app/Admin/routes.py
from flask import Blueprint, request, jsonify
from Admin.decorators import jwt_role_required
from Admin.schemas import DepartmentSchema
from Admin.services import admin_service

admin_bp = Blueprint("admin", __name__)

# Create department
@admin_bp.route("/departments", methods=["POST"])
@jwt_role_required(["admin"])
def create_department():
    payload = request.get_json(silent=True)
    if not payload or "name" not in payload:
        return jsonify({"msg": "Department name is required"}), 400

    schema = DepartmentSchema()
    errors = schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    try:
        dept = admin_service.create_department(payload["name"])
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

    return jsonify(schema.dump(dept)), 201


# List departments
@admin_bp.route("/departments", methods=["GET"])
@jwt_role_required(["admin"])
def list_departments():
    depts = admin_service.list_departments()
    schema = DepartmentSchema(many=True)
    return jsonify(schema.dump(depts)), 200


# Onboard doctor
@admin_bp.route("/doctors", methods=["POST"])
@jwt_role_required(["admin"])
def onboarding_doctor():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"msg": "Missing JSON payload"}), 400

    required_fields = ["username", "email", "password"]
    for field in required_fields:
        if not payload.get(field):
            return jsonify({"msg": f"{field} is required"}), 400

    doctor = admin_service.onboard_doctor(
        payload["username"], payload["email"], payload["password"]
    )
    return jsonify({
        "id": doctor.id,
        "username": doctor.username,
        "role": doctor.role
    }), 201

# ------------------------
# Assign doctor to department
# ------------------------
@admin_bp.route("/doctors/assign", methods=["POST"])
@jwt_role_required(["admin"])
def assign_doctor():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"msg": "Missing JSON payload"}), 400

    doctor_id = payload.get("doctor_id")
    department_id = payload.get("department_id")

    if not doctor_id or not department_id:
        return jsonify({"msg": "doctor_id and department_id are required"}), 400

    assoc = admin_service.assign_doctor_to_department(int(doctor_id), int(department_id))
    return jsonify({
        "id": assoc.id,
        "doctor_id": assoc.doctor_id,
        "department_id": assoc.department_id
    }), 200
