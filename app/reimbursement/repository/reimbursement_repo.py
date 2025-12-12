from app.config.database import db
from app.reimbursement.models.reimbursement import Reimbursement

class ReimbursementRepository:

    @staticmethod
    def create(member_id, appointment_id, amount, description):
        r = Reimbursement(
            member_id=member_id,
            appointment_id=appointment_id,
            amount=amount,
            description=description,
            status="Pending"
        )
        db.session.add(r)
        db.session.commit()
        return r

    @staticmethod
    def get_by_member(member_id):
        return Reimbursement.query.filter_by(member_id=member_id).all()

    @staticmethod
    def get_all():
        return Reimbursement.query.all()

    @staticmethod
    def update_status(claim_id, status):
        r = Reimbursement.query.get(claim_id)
        if not r:
            return None
        r.status = status
        db.session.commit()
        return r