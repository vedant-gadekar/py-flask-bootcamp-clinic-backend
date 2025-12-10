from flask import Blueprint, request, jsonify, g
from app.admin.services.department_services import DepartmentService
from app.admin.services.doctor_services import DoctorService
from app.common.utils.rbac_decorator import requires_role
from app.admin.schemas.department_schema import DepartmentSchema
from app.admin.schemas.doctor_schema import OnboardDoctorSchema, DoctorSchema 
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


admin_bp = Blueprint("admin", __name__)

department_schema = DepartmentSchema(many=True)
onboard_doctor_schema = OnboardDoctorSchema()
doctor_schema = DoctorSchema()

@requires_role("admin")
@admin_bp.get("/")
def admin_root():
    return {"message": "admin works"}

@admin_bp.route("/departments", methods=["POST"])
@requires_role("admin")
def create_department():
    data = request.get_json() or {}
    name = data.get("name")
    description = data.get("description")
    department = DepartmentService.create_department(name, description)
    return {"id": department.id, "name": department.name}, 201


@admin_bp.route("/departments", methods=["GET"])
@requires_role("admin")
def list_departments():
    departments = DepartmentService.list_departments()
    return department_schema.dump(departments), 200


@admin_bp.route("/doctors", methods=["POST"])
@requires_role("admin")
def onboard_doctor():
    try:
        data = onboard_doctor_schema.load(request.get_json())

        name = data["name"]
        email = data["email"]
        password = data["password"]
        specialization = data.get("specialization")
        experience_years = data.get("experience_years")

        doctor = DoctorService.onboard_doctor(
            name=name,
            email=email,
            password=password,
            specialization=specialization,
            experience_years=experience_years,
        )

        return doctor_schema.dump(doctor), 201

    except ValidationError as e:
        return jsonify(e.messages), 400
    except ValueError as e:
        return jsonify({"message": str(e)}), 400  
    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500

@admin_bp.route("/doctors", methods=["GET"])
@requires_role("admin")
def list_doctors():
    doctors = DoctorService.list_doctors()
    return doctor_schema.dump(doctors, many=True), 200

@admin_bp.route("/doctors/assign-department", methods=["POST"])
@requires_role("admin")
def assign_doctor_to_department():
    try:
        data = request.get_json() or {}
        doctor_id = data.get("doctor_id")
        department_id = data.get("department_id")

        if not doctor_id or not department_id:
            return jsonify({"message": "doctor_id and department_id are required"}), 400

        doctor = DoctorService.assign_doctor_to_department(doctor_id, department_id)

        return doctor_schema.dump(doctor), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    except SQLAlchemyError:
        return jsonify({"message": "Something went wrong"}), 500
