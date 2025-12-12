from app.appointment.models.appointment import Appointment
from app.config.database import db

class AppointmentRepository:

    @staticmethod
    def create(member_id, doctor_id, start, end):
        appt = Appointment(
            member_id=member_id,
            doctor_id=doctor_id,
            start_time=start,
            end_time=end
        )
        db.session.add(appt)
        db.session.commit()
        return appt

    @staticmethod
    def get_conflicting_appointment(doctor_id, start, end):
        return Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.start_time < end,
            Appointment.end_time > start
        ).first()

    @staticmethod
    def create(member_id, doctor_id, start, end):
        appt = Appointment(
            member_id=member_id,
            doctor_id=doctor_id,
            start_time=start,
            end_time=end
        )
        db.session.add(appt)
        db.session.commit()
        return appt

    @staticmethod
    def get_member_appointments(member_id):
        return Appointment.query.filter_by(member_id=member_id).all()

    @staticmethod
    def get_doctor_appointments(doctor_id):
        return Appointment.query.filter_by(doctor_id=doctor_id).all()

    @staticmethod
    def get_all():
        return Appointment.query.all()
