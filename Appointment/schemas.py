# app/Appointment/schemas.py
from marshmallow import Schema, fields, validate

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    doctor_id = fields.Int(required=True)
    member_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    status = fields.Str(
        validate=validate.OneOf(["scheduled", "completed", "canceled"]),
        load_default="scheduled"
    )
    created_at = fields.DateTime(dump_only=True)
