from werkzeug.exceptions import BadRequest
from app.appointment.repository.appointment_repo import AppointmentRepository
from app.reimbursement.repository.reimbursement_repo import ReimbursementRepository

class ReimbursementService:

    @staticmethod
    def submit_claim(member_id, appointment_id, amount, description):
        
        if amount <= 0:
            raise BadRequest("Amount must be greater than 0.")
        
        appt = AppointmentRepository.get_by_id(appointment_id)
        
        if not appt:
            raise ValueError("Appointment not found.")

        if appt.member_id != member_id:
            raise ValueError("You cannot claim reimbursement for another member's appointment.")

        if appt.status == "Cancelled":
            raise ValueError("Appointment already cancelled.")


        return ReimbursementRepository.create(member_id, appointment_id, amount, description)

    @staticmethod
    def get_member_claims(member_id):
        return ReimbursementRepository.get_by_member(member_id)

    @staticmethod
    def get_all_claims():
        return ReimbursementRepository.get_all()

    @staticmethod
    def approve_claim(claim_id):
        claim = ReimbursementRepository.update_status(claim_id, "Approved")
        if not claim:
            raise BadRequest("Claim not found.")
        return claim

    @staticmethod
    def reject_claim(claim_id):
        claim = ReimbursementRepository.update_status(claim_id, "Rejected")
        if not claim:
            raise BadRequest("Claim not found.")
        return claim
