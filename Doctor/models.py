#app/Doctor/models.py
from extensions import db
from datetime import datetime

class DoctorAvailability(db.Model):
    __tablename__ = "doctor_availabilities"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("User", backref=db.backref("availabilities", lazy=True))
