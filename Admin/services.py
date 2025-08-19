# app/Admin/services.py
from typing import Optional
from Admin.repositories import user_repo, dept_repo, doc_dept_repo
from Admin.models import ROLE_DOCTOR


class AuthService:
    def __init__(self, users=user_repo):
        self.users = users

    def register_user(self, username: str, email: str, password: str, role: str):
        existing = self.users.find_by_username(username)
        if existing:
            raise ValueError("Username already exists")
        return self.users.create_user(username, email, password, role)

    def authenticate(self, username: str, password: str):
        user = self.users.find_by_username(username)
        if not user or not user.check_password(password):
            return None
        return user


class AdminService:
    def __init__(self, users=user_repo, departments=dept_repo, doctor_departments=doc_dept_repo):
        self.users = users
        self.departments = departments
        self.doctor_departments = doctor_departments

    def create_department(self, name: str):
        return self.departments.create_department(name)

    def list_departments(self):
        return self.departments.list_departments()

    def onboard_doctor(self, username: str, email: str, password: str):
        return self.users.create_user(username, email, password, ROLE_DOCTOR)

    def assign_doctor_to_department(self, doctor_id: int, dept_id: int):
        #validate existence here in future
        return self.doctor_departments.assign_doctor(doctor_id, dept_id)

    def list_doctors(self):
        return self.users.get_users_by_role(ROLE_DOCTOR)


# Service singletons to import in routes
auth_service = AuthService()
admin_service = AdminService()
