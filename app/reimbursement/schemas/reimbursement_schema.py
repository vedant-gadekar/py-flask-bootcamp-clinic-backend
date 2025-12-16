from marshmallow import Schema, fields
from app.reimbursement.models.reimbursement import ClaimStatus
from enum import Enum


class ReimbursementCreateSchema(Schema):
    appointment_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    description = fields.Str(required=False)


class ReimbursementResponseSchema(Schema):
    id = fields.Int()
    member_id = fields.Int()
    appointment_id = fields.Int()
    amount = fields.Float()
    description = fields.Str()
    status = fields.Method("get_status")
    created_at = fields.DateTime()
    def get_status(self, obj):
        return obj.status.value
