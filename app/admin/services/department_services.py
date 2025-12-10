from app.admin.repository.department_repo import DepartmentRepository


class DepartmentService:
    @staticmethod
    def create_department(name, description):
        return DepartmentRepository.create(name, description)

    @staticmethod
    def list_departments():
        return DepartmentRepository.list_all()
    
    
    

