#app/Appointment/models.py
from extensions import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="scheduled")  # scheduled, completed, canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("User", foreign_keys=[doctor_id], backref=db.backref("appointments", lazy=True))
    member = db.relationship("User", foreign_keys=[member_id], backref=db.backref("member_appointments", lazy=True))
