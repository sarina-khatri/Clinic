# app/services.py
from .repositories import UserRepository, DepartmentRepository, DoctorDepartmentRepository
from .models import ROLE_ADMIN

class AuthService:
    @staticmethod
    def register_user(username, email, password, role):
        existing = UserRepository.find_by_username(username)
        if existing:
            raise ValueError("Username already exists")
        return UserRepository.create_user(username, email, password, role)

    @staticmethod
    def authenticate(username, password):
        user = UserRepository.find_by_username(username)
        if not user or not user.check_password(password):
            return None
        return user

class AdminService:
    @staticmethod
    def create_department(name):
        return DepartmentRepository.create_department(name)

    @staticmethod
    def list_departments():
        return DepartmentRepository.list_departments()

    @staticmethod
    def onboard_doctor(username, email, password):
        return UserRepository.create_user(username, email, password, "doctor")

    @staticmethod
    def assign_doctor_to_department(doctor_id, dept_id):
        return DoctorDepartmentRepository.assign_doctor(doctor_id, dept_id)

    @staticmethod
    def list_doctors():
        return UserRepository.get_users_by_role("doctor")

