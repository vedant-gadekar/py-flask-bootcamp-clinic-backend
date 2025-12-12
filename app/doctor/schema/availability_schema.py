from app.config.database import ma
from app.doctor.models.doctor_availability import DoctorAvailability
from marshmallow import validates, fields


class AvailabilitySchema(ma.SQLAlchemyAutoSchema):
    start_time = fields.Integer(required=True)
    end_time = fields.Integer(required=True)
    doctor_id = fields.Integer(dump_only=True)

    class Meta:
        model = DoctorAvailability
        include_fk = True
        load_instance = False