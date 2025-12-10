from app.config.database import ma
from app.admin.models.department import Department


class DepartmentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Department
        load_instance = True
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    created_at = ma.auto_field()


