# app/Admin/models.py
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

ROLE_ADMIN = "admin"
ROLE_DOCTOR = "doctor"
ROLE_MEMBER = "member"
# use enum


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default=ROLE_MEMBER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)


class DoctorDepartment(db.Model):
    __tablename__ = "doctor_departments"
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
