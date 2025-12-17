from flask import Blueprint, request, jsonify, g
from app.admin.services.department_services import DepartmentService
from app.admin.services.doctor_services import DoctorService
from app.common.models.user import RoleEnum
from app.common.utils.decorators import requires_role
from app.admin.schemas.department_schema import DepartmentSchema
from app.admin.schemas.doctor_schema import OnboardDoctorSchema, DoctorSchema , AssignDoctorDepartmentSchema
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.common.utils.decorators import feature_flag_required


admin_bp = Blueprint("admin", __name__)

department_schema_many = DepartmentSchema(many=True)
department_schema_single = DepartmentSchema()
onboard_doctor_schema = OnboardDoctorSchema()
assign_department_schema = AssignDoctorDepartmentSchema()
doctor_schema = DoctorSchema()

@requires_role(RoleEnum.ADMIN)
@admin_bp.get("/")
def admin_root():
    return {"message": "admin works"}


@admin_bp.route("/departments", methods=["POST"])
@requires_role(RoleEnum.ADMIN)
@feature_flag_required("create_department")
def create_department():
    try:
        data = department_schema_single.load(request.get_json() or {})
        
        department = DepartmentService.create_department(
            name=data.name, 
            description=data.description    
        )
        
        return department_schema_single.dump(department), 201
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400  


@admin_bp.route("/departments", methods=["GET"])
@requires_role(RoleEnum.ADMIN)
@feature_flag_required("list_departments")
def list_departments():
    departments = DepartmentService.list_departments()
    return department_schema_many.dump(departments), 200


@admin_bp.route("/doctors", methods=["POST"])
@requires_role(RoleEnum.ADMIN)
@feature_flag_required("create_doctor")
def onboard_doctor():
    try:
        data = onboard_doctor_schema.load(request.get_json())

        doctor = DoctorService.onboard_doctor(
            name = data["name"],
            email = data["email"],
            password = data["password"],
            specialization = data.get("specialization"),
            experience_years = data.get("experience_years")
        )

        return doctor_schema.dump(doctor), 201

    except ValidationError as e:
        return jsonify(e.messages), 400
    except ValueError as e:
        return jsonify({"message": str(e)}), 400  
    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500


@admin_bp.route("/doctors", methods=["GET"])
@requires_role(RoleEnum.ADMIN)
@feature_flag_required("list_doctors")
def list_doctors():
    doctors = DoctorService.list_doctors()
    return doctor_schema.dump(doctors, many=True), 200

@admin_bp.route("/doctors/assign-department", methods=["POST"])
@requires_role(RoleEnum.ADMIN)
@feature_flag_required("assign_doctor")
def assign_doctor_to_department():
    try:
        data = assign_department_schema.load(request.get_json() or {})
          
        doctor = DoctorService.assign_doctor_to_department(
            doctor_id=data["doctor_id"], 
            department_id=data["department_id"]
        )

        return doctor_schema.dump(doctor), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500
