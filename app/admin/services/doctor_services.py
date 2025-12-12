from app.admin.repository.department_repo import DepartmentRepository
from app.common.models.user import RoleEnum
from app.common.repository.user_repo import UserRepository
from app.admin.repository.doctor_repo import DoctorRepository
from app.common.utils.password_hash import hash_password

class DoctorService:
    @staticmethod
    def onboard_doctor(name, email, password,specialization=None, experience_years=None):
        existing = UserRepository.get_by_email(email)
        if existing:
            if existing.role ==RoleEnum.DOCTOR:
                raise ValueError("Doctor already onboarded")

            if existing.role == RoleEnum.MEMBER or existing.role == RoleEnum.ADMIN:
                UserRepository.update_role(existing.id, RoleEnum.DOCTOR)
                doctor = DoctorRepository.create_doctor(
                    user_id=existing.id,
                    name=name,
                    specialization=specialization,
                    experience_years=experience_years,
                )
                return doctor
            raise ValueError("Email already registered")

        user = UserRepository.create_user(
            email=email,
            password=hash_password(password),
            role=RoleEnum.DOCTOR
        )

        doctor = DoctorRepository.create_doctor(
            user_id=user.id,
            name=name,
            specialization=specialization,
            experience_years=experience_years,
        )
        return doctor

    @staticmethod
    def assign_doctor_to_department(doctor_id: int, department_id: int):
        doctor = DoctorRepository.get_by_id(doctor_id)
        if not doctor:
            raise ValueError("Doctor not found")
        
        department = DepartmentRepository.get_by_id(department_id)
        if not department:
            raise ValueError("Department not found")

        assigned = DoctorRepository.assign_department(doctor, department_id)
        return assigned

    @staticmethod
    def list_doctors():
        return DoctorRepository.list_all()