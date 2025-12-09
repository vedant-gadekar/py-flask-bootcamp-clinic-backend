from app.config.db import db
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    MEMBER = "member"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=RoleEnum.MEMBER.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor_profile = db.relationship("DoctorProfile", back_populates="user", uselist=False)

class Department(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DoctorProfile(db.Model):
    __tablename__ = "doctor_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)
    qualifications = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.String(1000), nullable=True)

    user = db.relationship("User", back_populates="doctor_profile")
    department = db.relationship("Department")
