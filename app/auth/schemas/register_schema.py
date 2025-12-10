from app.config.database import ma
from marshmallow import fields, validate

class RegisterSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(validate=validate.OneOf(["admin","doctor","member"]), load_default="member")
    
