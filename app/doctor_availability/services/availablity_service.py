from datetime import datetime
from app.doctor_availability.repository.availability_repo import AvailabilityRepository
from werkzeug.exceptions import BadRequest

class AvailabilityService:

    @staticmethod
    def add_availability(doctor_id, start, end):
        existing = AvailabilityRepository.find_slot(doctor_id, start, end)

        if existing:
            raise BadRequest("Availability for this time slot already exists.")

        if start < 0 or start > 23:
            raise ValueError("Invalid start hour")

        if end <= start or end > 24:
            raise ValueError("Invalid end hour")
        
        return AvailabilityRepository.create(doctor_id, start, end)

    @staticmethod
    def delete_availability(doctor_id, slot_id):
        slot = AvailabilityRepository.delete(slot_id, doctor_id)
        if not slot:
            raise ValueError("Availability slot not found.")
        return slot
    
    @staticmethod
    def list_availability(doctor_id):
        return AvailabilityRepository.get_by_doctor(doctor_id)
