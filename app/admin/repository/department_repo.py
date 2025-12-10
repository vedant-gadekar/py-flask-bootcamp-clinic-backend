from app.admin.models.department import  Department
from app.config.database import db

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