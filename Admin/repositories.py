# app/Admin/repositories.py
from typing import Optional, List
from extensions import db
from Admin.models import User, Department, DoctorDepartment


class UserRepository:
    def create_user(self, username: str, email: str, password: str, role: str) -> User:
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def find_by_username(self, username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

    def find_by_id(self, user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    def get_users_by_role(self, role: str) -> List[User]:
        return User.query.filter_by(role=role).all()


class DepartmentRepository:
    def create_department(self, name: str) -> Department:
        dept = Department(name=name)
        db.session.add(dept)
        db.session.commit()
        return dept

    def list_departments(self) -> list[Department]:
        return Department.query.all()

    def find_by_id(self, dept_id: int) -> Optional[Department]:
        return Department.query.get(dept_id)


class DoctorDepartmentRepository:
    def assign_doctor(self, doctor_id: int, department_id: int) -> DoctorDepartment:
        assoc = DoctorDepartment(doctor_id=doctor_id, department_id=department_id)
        db.session.add(assoc)
        db.session.commit()
        return assoc

    def find_by_doctor(self, doctor_id: int) -> list[DoctorDepartment]:
        return DoctorDepartment.query.filter_by(doctor_id=doctor_id).all()


# Singletons (simple DI for app modules)
user_repo = UserRepository()
dept_repo = DepartmentRepository()
doc_dept_repo = DoctorDepartmentRepository()
