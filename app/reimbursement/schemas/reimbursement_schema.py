from app.config.database import ma
from app.reimbursement.models.reimbursement import Reimbursement
from marshmallow import fields

class ReimbursementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reimbursement
        include_fk = True
        load_instance = False

    id = fields.Integer(dump_only=True)
    member_id = fields.Integer(dump_only=True)
    status = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    appointment_id = fields.Integer(required=True)
    amount = fields.Float(required=True)
    description = fields.String(required=False)
