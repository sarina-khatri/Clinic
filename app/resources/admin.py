# app/resources/admin.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from ..decorators import jwt_or_session_role_required
from ..schemas import DepartmentSchema
from ..services import AdminService

admin_bp = Blueprint("admin", __name__)

#create dept.
@admin_bp.route("/departments", methods=["POST"])
@jwt_or_session_role_required(["admin"])
def create_department():
    if request.is_json:
        payload = request.get_json()
        schema = DepartmentSchema()
        errors = schema.validate(payload)
        if errors:
            return jsonify(errors), 400
        dept = AdminService.create_department(payload["name"])
        return jsonify(schema.dump(dept)), 201
    else:
        name = request.form.get("name")
        if not name:
            flash("Department name is required", "error")
            return redirect(url_for("admin.create_department_form"))
        AdminService.create_department(name)
        flash("Department created successfully", "success")
        return redirect(url_for("auth.dashboard"))

#list dept.
@admin_bp.route("/departments", methods=["GET"])
@jwt_or_session_role_required(["admin"])
def list_departments():
    depts = AdminService.list_departments()
    if request.accept_mimetypes.accept_html:
        return render_template("list_departments.html", departments=depts)
    else:
        schema = DepartmentSchema(many=True)
        return jsonify(schema.dump(depts)), 200

#add doctor
@admin_bp.route("/doctors", methods=["POST"])
@jwt_or_session_role_required(["admin"])
def onboarding_doctor():
    if request.is_json:
        payload = request.get_json()
        if not payload.get("username") or not payload.get("email") or not payload.get("password"):
            return jsonify({"msg": "username, email, password required"}), 400
        doctor = AdminService.onboard_doctor(payload["username"], payload["email"], payload["password"])
        return jsonify({"id": doctor.id, "username": doctor.username, "role": doctor.role}), 201
    else:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not username or not email or not password:
            flash("All fields are required", "error")
            return redirect(url_for("admin.onboard_doctor_form"))
        AdminService.onboard_doctor(username, email, password)
        flash("Doctor onboarded successfully", "success")
        return redirect(url_for("auth.dashboard"))

#assign doc to dept.
@admin_bp.route("/doctors/assign", methods=["POST"])
@jwt_or_session_role_required(["admin"])
def assign_doctor():
    if request.is_json:
        payload = request.get_json()
        doctor_id = payload.get("doctor_id")
        department_id = payload.get("department_id")
    else:
        doctor_id = request.form.get("doctor_id")
        department_id = request.form.get("department_id")

    if not doctor_id or not department_id:
        msg = "doctor_id and department_id are required"
        if request.is_json:
            return jsonify({"msg": msg}), 400
        else:
            flash(msg, "error")
            return redirect(url_for("admin.assign_doctor_form"))

    assoc = AdminService.assign_doctor_to_department(int(doctor_id), int(department_id))

    if request.is_json:
        return jsonify({"id": assoc.id, "doctor_id": assoc.doctor_id, "department_id": assoc.department_id}), 200
    else:
        flash("Doctor assigned to department successfully", "success")
        return redirect(url_for("auth.dashboard"))

# admin dashboard HTML form routes
@admin_bp.route("/departments/new", methods=["GET"])
@jwt_or_session_role_required(["admin"])
def create_department_form():
    return render_template("create_department.html")

@admin_bp.route("/doctors/new", methods=["GET"])
@jwt_or_session_role_required(["admin"])
def onboard_doctor_form():
    return render_template("onboard_doctor.html")

@admin_bp.route("/assign", methods=["GET"])
@jwt_or_session_role_required(["admin"])
def assign_doctor_form():
    departments = AdminService.list_departments()
    doctors = AdminService.list_doctors()
    return render_template("assign_doctor.html", departments=departments, doctors=doctors)
