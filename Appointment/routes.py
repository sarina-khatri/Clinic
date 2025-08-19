#app/Appointment/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from Appointment.models import Appointment
from Appointment.schemas import AppointmentSchema
from extensions import db
from Admin.decorators import jwt_role_required
from datetime import datetime
from common.scheduling import is_doctor_available

appointment_bp = Blueprint("appointment", __name__)

# Member can book an appointment
@appointment_bp.route("/book", methods=["POST"])
@jwt_role_required(["member"])
def book_appointment():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"msg": "Missing JSON payload"}), 400

    member_id = get_jwt_identity()
    payload["member_id"] = member_id

    schema = AppointmentSchema()
    errors = schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    doctor_id = payload["doctor_id"]
    start_time = datetime.fromisoformat(payload["start_time"])
    end_time = datetime.fromisoformat(payload["end_time"])

    available, msg = is_doctor_available(doctor_id, start_time, end_time)
    if not available:
        return jsonify({"msg": msg}), 400

    appointment = Appointment(
        doctor_id=doctor_id,
        member_id=member_id,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify(schema.dump(appointment)), 201

# Member can view their appointments
@appointment_bp.route("/my", methods=["GET"])
@jwt_role_required(["member"])
def my_appointments():
    member_id = get_jwt_identity()
    appointments = Appointment.query.filter_by(member_id=member_id).all()
    schema = AppointmentSchema(many=True)
    return jsonify(schema.dump(appointments)), 200

# Admin can view all appointments
@appointment_bp.route("/all", methods=["GET"])
@jwt_role_required(["admin"])
def all_appointments():
    appointments = Appointment.query.all()
    schema = AppointmentSchema(many=True)
    return jsonify(schema.dump(appointments)), 200
