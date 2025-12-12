from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.utils.rbac_decorator import requires_role
from app.doctor.services.availablity_service import AvailabilityService
from app.doctor.schema.availability_schema import AvailabilitySchema
from datetime import datetime

availability_bp = Blueprint("availability_bp", __name__)

@availability_bp.route("", methods=["POST"])
@requires_role("doctor")
def add_availability():
    
    data = AvailabilitySchema().load(request.get_json())

    start = data["start_time"]
    end = data["end_time"]

    doctor_id = get_jwt_identity()

    slot = AvailabilityService.add_availability(doctor_id, start, end)
    return jsonify({"message": "Availability added", "id": slot.id}), 201



@availability_bp.route("/list", methods=["GET"])
@requires_role("doctor")
def list_availability():
    doctor_id = get_jwt_identity()

    schema=AvailabilitySchema(many=True)
    slots = AvailabilityService.list_availability(doctor_id)
    return jsonify(schema.dump(slots)), 200
