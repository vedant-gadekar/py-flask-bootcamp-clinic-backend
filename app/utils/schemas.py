from app.config.db import db,ma
from app.models.models import User, Department, Doctor
from marshmallow import fields, validate

class RegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(validate=validate.OneOf(["admin","doctor","member"]), load_default="member")

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
    id = ma.auto_field()
    email = ma.auto_field()
    role = ma.auto_field()
    created_at = ma.auto_field()
    
class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class DepartmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Department
        load_instance = True
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()


class OnboardDoctorSchema(ma.Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    specialization = fields.Str(required=False)
    experience_years = fields.Int(required=False)

class DoctorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Doctor
        include_fk = True
        load_instance = True

    email = fields.Method("get_email")

    def get_email(self, obj):
        return obj.user.email if obj.user else None
