#app/Doctor/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from Doctor.models import DoctorAvailability
from Doctor.schemas import DoctorAvailabilitySchema
from extensions import db
from Admin.decorators import jwt_role_required
from datetime import datetime
from common.scheduling import is_doctor_available

doctor_bp = Blueprint("doctor", __name__)

# Add availability (Doctor only)
@doctor_bp.route("/availability", methods=["POST"])
@jwt_role_required(["doctor"])
def add_availability():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"msg": "Missing JSON payload"}), 400

    schema = DoctorAvailabilitySchema()
    errors = schema.validate(payload)
    if errors:
        return jsonify(errors), 400

    doctor_id = get_jwt_identity()
    date = datetime.strptime(payload["date"], "%Y-%m-%d").date()
    start_time = datetime.strptime(payload["start_time"], "%H:%M:%S").time()
    end_time = datetime.strptime(payload["end_time"], "%H:%M:%S").time()

    # Prevent overlapping slots
    overlapping = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.date == date,
        DoctorAvailability.start_time < end_time,
        DoctorAvailability.end_time > start_time
    ).first()
#route should not query directly
    if overlapping:
        return jsonify({"msg": "This time slot overlaps with existing availability"}), 400

    availability = DoctorAvailability(
        doctor_id=doctor_id,
        date=date,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(availability)
    db.session.commit()
    return jsonify(schema.dump(availability)), 201

# List availability (Doctor only)
@doctor_bp.route("/availability", methods=["GET"])
@jwt_role_required(["doctor"])
def list_availability():
    doctor_id = get_jwt_identity()
    availabilities = DoctorAvailability.query.filter_by(doctor_id=doctor_id).all()
    schema = DoctorAvailabilitySchema(many=True)
    return jsonify(schema.dump(availabilities)), 200

# Update availability (Doctor only)
@doctor_bp.route("/availability/<int:availability_id>", methods=["PUT"])
@jwt_role_required(["doctor"])
def update_availability(availability_id):
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"msg": "Missing JSON payload"}), 400

    schema = DoctorAvailabilitySchema()
    errors = schema.validate(payload, partial=True)
    if errors:
        return jsonify(errors), 400

    doctor_id = get_jwt_identity()
    availability = DoctorAvailability.query.filter_by(id=availability_id, doctor_id=doctor_id).first()
    if not availability:
        return jsonify({"msg": "Availability not found"}), 404

    if "date" in payload:
        availability.date = datetime.strptime(payload["date"], "%Y-%m-%d").date()
    if "start_time" in payload:
        availability.start_time = datetime.strptime(payload["start_time"], "%H:%M:%S").time()
    if "end_time" in payload:
        availability.end_time = datetime.strptime(payload["end_time"], "%H:%M:%S").time()

    start_datetime = datetime.combine(availability.date, availability.start_time)
    end_datetime = datetime.combine(availability.date, availability.end_time)

    available, msg = is_doctor_available(
        doctor_id, start_datetime, end_datetime, exclude_availability_id=availability.id
    )
    if not available:
        return jsonify({"msg": msg}), 400

    db.session.commit()
    return jsonify(schema.dump(availability)), 200

# Delete availability (Doctor only)
@doctor_bp.route("/availability/<int:availability_id>", methods=["DELETE"])
@jwt_role_required(["doctor"])
def delete_availability(availability_id):
    doctor_id = get_jwt_identity()
    availability = DoctorAvailability.query.filter_by(id=availability_id, doctor_id=doctor_id).first()
    if not availability:
        return jsonify({"msg": "Availability not found"}), 404

    db.session.delete(availability)
    db.session.commit()
    return jsonify({"msg": "Availability deleted successfully"}), 200

# Admin sees all
@doctor_bp.route("/all", methods=["GET"])
@jwt_role_required(["admin"])
def all_availabilities():
    availabilities = DoctorAvailability.query.all()
    schema = DoctorAvailabilitySchema(many=True)
    return jsonify(schema.dump(availabilities)), 200
