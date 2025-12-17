from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.common.utils.decorators import requires_role
from app.appointment.services.appointment_service import AppointmentService
from app.appointment.schemas.appointment_schema import AppointmentSchema
from app.common.models.user import RoleEnum
from app.appointment.models.appointment import Appointment as appointment
from app.common.utils.decorators import feature_flag_required

appointment_bp = Blueprint("appointment_bp", __name__)

@appointment_bp.route("/book", methods=["POST"])
@requires_role(RoleEnum.MEMBER)
@feature_flag_required("book_appointment")
def book_appointment():
    raw_data = request.get_json()
    try:
        data = AppointmentSchema().load(raw_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    member_id = get_jwt_identity()
    doctor_id = data["doctor_id"]
    start = data["start_time"]
    end = data["end_time"]
    try:
        appt = AppointmentService.book(member_id, doctor_id, start, end)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
     
    return AppointmentSchema(many=True).jsonify([appt]), 201
        

@appointment_bp.route("/my", methods=["GET"])
@requires_role(RoleEnum.MEMBER)
@feature_flag_required("list_member_appointments")
def my_appointments():
    member_id = get_jwt_identity()
    try:
        appts = AppointmentService.member_appointments(member_id)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    return AppointmentSchema(many=True).jsonify(appts), 200


@appointment_bp.route("/doctor", methods=["GET"])
@requires_role(RoleEnum.DOCTOR)
@feature_flag_required("list_doctor_appointments")
def doctor_appointments():
    doctor_id = get_jwt_identity()
    try:
        appts = AppointmentService.doctor_appointments(doctor_id)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    return AppointmentSchema(many=True).jsonify(appts),200


@appointment_bp.route("/admin", methods=["GET"])
@requires_role(RoleEnum.ADMIN)
@feature_flag_required("view_appointments")
def admin_appointments():
    try:
        appts = AppointmentService.admin_all_appointments()
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    return AppointmentSchema(many=True).jsonify(appts), 200

@appointment_bp.route("/cancel", methods=["PUT"])
@requires_role(RoleEnum.MEMBER)
@feature_flag_required("cancel_appointment")
def cancel_appointment():
    member_id = int(get_jwt_identity())
    data = request.get_json() or {}
    
    appointment_id = data.get("appointment_id")
    if not appointment_id:
        return jsonify({"error": "appointment_id is required"}), 400

    try:
        appt = AppointmentService.cancel_appointment(
            appointment_id=appointment_id,
            member_id=member_id
        )
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    return AppointmentSchema().jsonify(appt), 200
