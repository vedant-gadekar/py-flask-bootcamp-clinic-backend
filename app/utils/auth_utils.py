import datetime
from flask_jwt_extended import create_access_token, create_refresh_token,get_jwt, verify_jwt_in_request
from functools import wraps
from flask import request, current_app, jsonify, g
from passlib.context import CryptContext
from app.models.models import User
from app.config.db import db

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    if(plain is None):
        raise ValueError("Password cannot be null")
    return pwd_ctx.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def generate_token(identity, role):
    access_token = create_access_token(
        identity=str(identity), additional_claims={"role": role}, expires_delta=datetime.timedelta(hours=1)
    )

    refresh_token = create_refresh_token(
        identity=str(identity), additional_claims={"role": role}, expires_delta=datetime.timedelta(days=30)
    )

    return access_token, refresh_token

def requires_role(*allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({"error": "Unauthorized. Insufficient role."}), 403

            return fn(*args, **kwargs)

        return decorated

    return wrapper



