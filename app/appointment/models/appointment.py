from app.config.database import db
from datetime import datetime


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.CheckConstraint("start_time >= 0 AND start_time <= 23"),
        db.CheckConstraint("end_time > start_time"),
        db.CheckConstraint("end_time >= 1 AND end_time <= 24"),
        db.UniqueConstraint("doctor_id", "start_time", "end_time"),
    )
