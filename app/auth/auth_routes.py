from flask import Blueprint, request, jsonify
from app.utils.schemas import LoginSchema, UserSchema, RegisterSchema
from app.services.auth_service import AuthService
from marshmallow import ValidationError

auth_bp = Blueprint("auth", __name__)
register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()


@auth_bp.get("/")
def auth_root():
    return {"message": "auth works"}

@auth_bp.route("/register", methods=["POST"])
def register():
    json_data = request.get_json() or {}
    try:
        data = register_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        user = AuthService.register_user(
            email=data["email"], 
            password=data["password"],
            role=data.get("role", "member")
            )
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    return user_schema.dump(user), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = login_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    email = data["email"]
    password = data["password"]

    try:
        access_token, refresh_token, user = AuthService.login_user(email, password)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role
        }, 200
    except ValueError as e:
        return {"message": str(e)}, 401



