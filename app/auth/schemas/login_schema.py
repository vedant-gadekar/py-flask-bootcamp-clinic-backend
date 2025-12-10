from app.config.database import db,ma
from marshmallow import fields

class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)