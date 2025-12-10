from app.config.database import db
from datetime import datetime
from enum import Enum

class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(120))
    experience_years = db.Column(db.Integer)

    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)
    department = db.relationship("Department", back_populates="doctors")

    user = db.relationship("User")