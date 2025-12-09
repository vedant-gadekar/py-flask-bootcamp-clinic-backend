from app.models.models import Doctor
from app.config.db import db


class DoctorRepository:

    @staticmethod
    def create_doctor(user_id: int, name: str, specialization=None, experience_years=None):
        doctor = Doctor(
            user_id=user_id,
            name=name,
            specialization=specialization,
            experience_years=experience_years,
        )
        db.session.add(doctor)
        db.session.commit()
        return doctor

    @staticmethod
    def get_by_id(doctor_id: int):
        return Doctor.query.get(doctor_id)

    @staticmethod
    def list_all():
        return Doctor.query.all()

    @staticmethod
    def assign_department(doctor: Doctor, department_id: int):
        doctor.department_id = department_id
        db.session.commit()
        return doctor

    @staticmethod
    def delete_doctor(doctor: Doctor):
        db.session.delete(doctor)
        db.session.commit()

    @staticmethod
    def update_doctor(doctor: Doctor, **kwargs):
        for key, value in kwargs.items():
            setattr(doctor, key, value)
        db.session.commit()
        return doctor
