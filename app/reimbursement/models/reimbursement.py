from app.config.database import db
from enum import Enum
from datetime import datetime

class StatusEnum(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class Reimbursement(db.Model):
    __tablename__ = "reimbursements"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=StatusEnum.PENDING)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    member = db.relationship("User", backref="reimbursements")
    appointment = db.relationship("Appointment", backref="reimbursements")
   

    

    