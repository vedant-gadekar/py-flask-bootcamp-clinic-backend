from app.config.database import ma
from app.common.models.user import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
    id = ma.auto_field()
    email = ma.auto_field()
    role = ma.auto_field()
    created_at = ma.auto_field()