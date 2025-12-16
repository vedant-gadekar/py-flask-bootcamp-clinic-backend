from app.doctor_availability.repository.availability_repo import AvailabilityRepository
from app.appointment.repository.appointment_repo import AppointmentRepository
from app.appointment.models.appointment import AppointmentStatusEnum

class AppointmentService:

    @staticmethod
    def book(member_id, doctor_id, start, end):

        if start >= end:
            raise ValueError("Invalid time range.")


        availability = AvailabilityRepository.get_by_doctor(doctor_id)
        valid_slot = next(
            (slot for slot in availability if slot.start_time <= start and slot.end_time >= end),
            None
        )

        if not valid_slot:
            raise ValueError("Doctor is not available during this time.")


        conflict = AppointmentRepository.get_conflicting_appointment(doctor_id, start, end)
        if conflict:
            raise ValueError("Doctor already has an appointment at this time.")
        
        appt = AppointmentRepository.create(member_id, doctor_id, start, end)

        if valid_slot.start_time == start and valid_slot.end_time == end:
            AvailabilityRepository.delete(valid_slot)

        elif valid_slot.start_time==start:
            valid_slot.start_time = end
            AvailabilityRepository.update()
        
        elif valid_slot.end_time==end:
            valid_slot.end_time = start
            AvailabilityRepository.update()
        else:
            AvailabilityRepository.create(
                doctor_id,
                end,                 
                valid_slot.end_time  
            )
            valid_slot.end_time = start  
            AvailabilityRepository.update()

        return appt

    @staticmethod
    def member_appointments(member_id):
        return AppointmentRepository.get_member_appointments(member_id)

    @staticmethod
    def doctor_appointments(doctor_id):
        return AppointmentRepository.get_doctor_appointments(doctor_id)

    @staticmethod
    def admin_all_appointments():
        return AppointmentRepository.get_all()
    
    @staticmethod
    def cancel_appointment(appointment_id, member_id):
        appointment = AppointmentRepository.get_by_id(appointment_id)
        print("appointment id:", appointment_id, type(appointment_id))

        if not appointment:
            raise ValueError("Appointment not found")

        if appointment.member_id != member_id:
            raise ValueError("You can cancel only your own appointment")

        if appointment.status == AppointmentStatusEnum.CANCELED.value:
            raise ValueError("Appointment already canceled")

        appointment.status = AppointmentStatusEnum.CANCELED.value

        return AppointmentRepository.save(appointment)

