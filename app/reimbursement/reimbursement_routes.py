from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.common.utils.rbac_decorator import requires_role
from app.reimbursement.schemas.reimbursement_schema import ReimbursementSchema
from app.reimbursement.services.reimbursement_service import ReimbursementService

reimbursement_bp = Blueprint("reimbursement_bp", __name__)

@reimbursement_bp.route("", methods=["POST"])
@requires_role("member")
def submit_claim():
    raw = request.get_json()

    try:
        data = ReimbursementSchema().load(raw)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    member_id = get_jwt_identity()

    try:
        claim = ReimbursementService.submit_claim(
            member_id=member_id,
            appointment_id=data["appointment_id"],
            amount=data["amount"],
            description=data.get("description", "")
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return ReimbursementSchema().jsonify(claim), 201


@reimbursement_bp.route("/my", methods=["GET"])
@requires_role("member")
def my_claims():
    member_id = get_jwt_identity()

    claims = ReimbursementService.get_member_claims(member_id)
    return ReimbursementSchema(many=True).jsonify(claims), 200


@reimbursement_bp.route("/admin", methods=["GET"])
@requires_role("admin")
def admin_get_all_claims():
    claims = ReimbursementService.get_all_claims()
    return ReimbursementSchema(many=True).jsonify(claims), 200


@reimbursement_bp.route("/admin/approve/<int:claim_id>", methods=["PUT"])
@requires_role("admin")
def approve_claim(claim_id):
    try:
        claim = ReimbursementService.approve_claim(claim_id)
        return ReimbursementSchema().jsonify(claim), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@reimbursement_bp.route("/admin/reject/<int:claim_id>", methods=["PUT"])
@requires_role("admin")
def reject_claim(claim_id):
    try:
        claim = ReimbursementService.reject_claim(claim_id)
        return ReimbursementSchema().jsonify(claim), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
