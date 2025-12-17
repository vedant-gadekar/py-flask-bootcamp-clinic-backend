from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.common.models.user import RoleEnum
from app.common.utils.decorators import requires_role
from app.doctor_availability.services.availablity_service import AvailabilityService
from app.doctor_availability.schema.availability_schema import AvailabilitySchema
from datetime import datetime
from app.common.utils.decorators import feature_flag_required

availability_bp = Blueprint("availability_bp", __name__)

@availability_bp.route("", methods=["POST"])
@requires_role(RoleEnum.DOCTOR)
@feature_flag_required("create_availability")
def add_availability():
    
    try:
        data = AvailabilitySchema().load(request.get_json())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


    start = data["start_time"]
    end = data["end_time"]
    doctor_id = get_jwt_identity()

    try:
        slot = AvailabilityService.add_availability(doctor_id, start, end)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400


    return AvailabilitySchema().jsonify(slot), 201

@availability_bp.route("/list", methods=["GET"])
@requires_role(RoleEnum.DOCTOR)
@feature_flag_required("get_availability")
def list_availability():
    doctor_id = get_jwt_identity()

    availability_schema=AvailabilitySchema(many=True)
    slots = AvailabilityService.list_availability(doctor_id)
    return jsonify(availability_schema.dump(slots)), 200
