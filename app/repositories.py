# app/repositories.py
from .extensions import db
from .models import User, Department, DoctorDepartment

class UserRepository:
    @staticmethod
    def create_user(username, email, password, role):
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_users_by_role(role):
        return User.query.filter_by(role=role).all()


class DepartmentRepository:
    @staticmethod
    def create_department(name):
        dept = Department(name=name)
        db.session.add(dept)
        db.session.commit()
        return dept

    @staticmethod
    def list_departments():
        return Department.query.all()

    @staticmethod
    def find_by_id(dept_id):
        return Department.query.get(dept_id)

class DoctorDepartmentRepository:
    @staticmethod
    def assign_doctor(doctor_id, department_id):
        assoc = DoctorDepartment(doctor_id=doctor_id, department_id=department_id)
        db.session.add(assoc)
        db.session.commit()
        return assoc

    @staticmethod
    def find_by_doctor(doctor_id):
        return DoctorDepartment.query.filter_by(doctor_id=doctor_id).all()
