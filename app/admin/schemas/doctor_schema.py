from app.config.database import ma
from app.admin.models.doctor import Doctor
from marshmallow import fields, validate

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
