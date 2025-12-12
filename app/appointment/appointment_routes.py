from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.utils.rbac_decorator import requires_role
from app.appointment.services.appointment_service import AppointmentService
from app.appointment.schemas.appointment_schema import AppointmentSchema

appointment_bp = Blueprint("appointment_bp", __name__)

@appointment_bp.route("/book", methods=["POST"])
@requires_role("member")
def book_appointment():
    raw_data = request.get_json()
    data=AppointmentSchema().load(raw_data)
    
    member_id = get_jwt_identity()
    doctor_id = data["doctor_id"]
    start = data["start_time"]
    end = data["end_time"]

    appt = AppointmentService.book(member_id, doctor_id, start, end)
    return jsonify({
        "message": "Appointment booked",
        "id": appt.id,
        "doctor_id": doctor_id,
        "start_time": start,
        "end_time": end
    }), 201


@appointment_bp.route("/my", methods=["GET"])
@requires_role("member")
def my_appointments():
    member_id = get_jwt_identity()
    appts = AppointmentService.member_appointments(member_id)
    return AppointmentSchema(many=True).jsonify(appts), 200


@appointment_bp.route("/doctor", methods=["GET"])
@requires_role("doctor")
def doctor_appointments():
    doctor_id = get_jwt_identity()
    appts = AppointmentService.doctor_appointments(doctor_id)
    return AppointmentSchema(many=True).jsonify(appts),200


@appointment_bp.route("/admin", methods=["GET"])
@requires_role("admin")
def admin_appointments():
    appts = AppointmentService.admin_all_appointments()
    return AppointmentSchema(many=True).jsonify(appts), 200

