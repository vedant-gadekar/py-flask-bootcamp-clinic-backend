from app.doctor.models.doctor_availability import DoctorAvailability
from app.config.database import db

class AvailabilityRepository:

    @staticmethod
    def create(doctor_id, start, end):
        slot = DoctorAvailability(
            doctor_id=doctor_id,
            start_time=start,
            end_time=end
        )
        db.session.add(slot)
        db.session.commit()
        return slot

    @staticmethod
    def get_by_doctor(doctor_id):
        return DoctorAvailability.query.filter_by(doctor_id=doctor_id).all()

    @staticmethod
    def delete(slot):
        db.session.delete(slot)
        db.session.commit()

    @staticmethod
    def find_slot(doctor_id, start, end):
        return (
            DoctorAvailability.query
            .filter_by(doctor_id=doctor_id, start_time=start, end_time=end)
            .first()
        )
        
    @staticmethod
    def update():
        db.session.commit()