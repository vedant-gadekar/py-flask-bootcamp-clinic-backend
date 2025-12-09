from flask import Blueprint, request, jsonify, g
from app.services.admin_service import AdminService
from app.utils.auth_utils import requires_role
from app.utils.schemas import DepartmentSchema, DoctorSchema, OnboardDoctorSchema
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
    department = AdminService.create_department(name, description)
    return {"id": department.id, "name": department.name}, 201


@admin_bp.route("/departments", methods=["GET"])
@requires_role("admin")
def list_departments():
    departments = AdminService.list_departments()
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

        doctor = AdminService.onboard_doctor(
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
    doctors = AdminService.list_doctors()
    return doctor_schema.dump(doctors, many=True), 200