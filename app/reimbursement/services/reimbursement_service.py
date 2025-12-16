from app.reimbursement.repository.reimbursement_repo import ReimbursementRepo
from app.reimbursement.models.reimbursement import ClaimStatus
from app.appointment.repository.appointment_repo import AppointmentRepository


class ReimbursementService:

    @staticmethod
    def submit_claim(member_id, appointment_id, amount, description):

        appointment = AppointmentRepository.get_by_id(appointment_id)
        if not appointment:
            raise ValueError("Appointment not found")

        if appointment.member_id != member_id:
            raise ValueError("You can only claim reimbursement for your own appointment")


        existing_claim = ReimbursementRepo.get_by_appointment_id(appointment_id)
        if existing_claim:
            raise ValueError("Reimbursement already requested for this appointment")

        if appointment.status != "Canceled":
            raise ValueError("Reimbursement can be requested only for canceled appointments")

        return ReimbursementRepo.create(
            member_id=member_id,
            appointment_id=appointment_id,
            amount=amount,
            description=description,
        )

    @staticmethod
    def review_claim(claim_id, status):
        try:
            status_enum = ClaimStatus[status]
        except KeyError:
            raise ValueError("Invalid status")

        claim = ReimbursementRepo.get_by_id(claim_id)
        if not claim:
            return None

        if claim.status != ClaimStatus.PENDING:
            raise ValueError("Claim has already been reviewed")

        return ReimbursementRepo.update_status(claim_id, status_enum)

    @staticmethod
    def get_claims():
        return ReimbursementRepo.get_all()
