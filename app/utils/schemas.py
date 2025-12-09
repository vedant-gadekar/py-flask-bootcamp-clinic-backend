from app.config.db import db,ma
from app.models.models import User, Department, DoctorProfile
from marshmallow import fields, validate

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
    id = ma.auto_field()
    email = ma.auto_field()
    role = ma.auto_field()
    created_at = ma.auto_field()

class RegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(validate=validate.OneOf(["admin","doctor","member"]), load_default="member")

class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class DepartmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Department
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()

class DoctorProfileSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DoctorProfile
    id = ma.auto_field()
    user_id = ma.auto_field()
    department_id = ma.auto_field()
    qualifications = ma.auto_field()
    bio = ma.auto_field()
