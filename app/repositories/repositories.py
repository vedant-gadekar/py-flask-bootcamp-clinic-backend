from app.models.models import User, Department, DoctorProfile
from app.config.db import db

class UserRepository:
    @staticmethod
    def create_user(email: str, password: str, role: str) -> User:
        user = User(email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id: int):
        return db.session.get(User, user_id)

class DepartmentRepository:
    @staticmethod
    def create(name: str, description: str = None):
        dept = Department(name=name, description=description)
        db.session.add(dept)
        db.session.commit()
        return dept

    @staticmethod
    def list_all():
        return Department.query.all()

    @staticmethod
    def get_by_id(dept_id: int):
        return db.session.get(Department, dept_id)

class DoctorRepository:
    @staticmethod
    def create_profile(user_id: int, department_id: int = None, qualifications: str = None, bio: str = None):
        prof = DoctorProfile(user_id=user_id, department_id=department_id, qualifications=qualifications, bio=bio)
        db.session.add(prof)
        db.session.commit()
        return prof
