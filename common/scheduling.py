#app/common/scheduling.py
from Doctor.models import DoctorAvailability
from Appointment.models import Appointment
from datetime import datetime

def is_doctor_available(doctor_id, start_datetime, end_datetime, exclude_availability_id=None):

    date = start_datetime.date()
    start_time = start_datetime.time()
    end_time = end_datetime.time()

    availability = DoctorAvailability.query.filter(
        DoctorAvailability.doctor_id == doctor_id,
        DoctorAvailability.date == date,
        DoctorAvailability.start_time <= start_time,
        DoctorAvailability.end_time >= end_time
    )

    if exclude_availability_id:
        availability = availability.filter(DoctorAvailability.id != exclude_availability_id)

    availability = availability.first()
    if not availability:
        return False, "Doctor is not available at this time"

    # Check overlapping appointments
    overlapping = Appointment.query.filter(
        Appointment.doctor_id == doctor_id,
        Appointment.start_time < end_datetime,
        Appointment.end_time > start_datetime
    ).first()
    if overlapping:
        return False, "This time slot is already booked"

    return True, None
