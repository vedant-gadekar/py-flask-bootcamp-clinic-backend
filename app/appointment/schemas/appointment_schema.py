from marshmallow import fields
from app.config.database import ma
from app.appointment.models.appointment import Appointment


class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        include_fk = True
        load_instance = False

    id = fields.Integer(dump_only=True)
    doctor_id = fields.Integer(dump_only=True)
    member_id = fields.Integer(dump_only=True)
    start_time = fields.Integer()
    end_time = fields.Integer()
