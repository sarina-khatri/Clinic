# Doctor/schemas.py
from marshmallow import Schema, fields

class DoctorAvailabilitySchema(Schema):
    id = fields.Int(dump_only=True)
    doctor_id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    created_at = fields.DateTime(dump_only=True)
