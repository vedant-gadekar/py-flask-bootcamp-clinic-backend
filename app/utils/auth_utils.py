import datetime
import jwt
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

def create_access_token(user_id: int, role: str):
    secret = current_app.config["JWT_SECRET_KEY"]
    algo = current_app.config["JWT_ALGORITHM"]
    exp_seconds = current_app.config["JWT_EXP_SECONDS"]
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_seconds),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, secret, algorithm=algo)
    return token

def decode_token(token: str):
    secret = current_app.config["JWT_SECRET"]
    algo = current_app.config["JWT_ALGORITHM"]
    return jwt.decode(token, secret, algorithms=[algo])

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"message": "Missing Authorization header"}), 401
        token = auth.split(" ", 1)[1]
        try:
            payload = decode_token(token)
            user_id = payload.get("sub")
            role = payload.get("role")
            user = db.session.get(User, user_id)
            if not user:
                return jsonify({"message": "User not found"}), 401
            # attach user to flask.g for handlers
            g.current_user = user
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
    return decorated

def requires_role(*allowed_roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(g, "current_user", None)
            if user is None:
                return jsonify({"message": "Unauthorized"}), 401
            if user.role not in allowed_roles:
                return jsonify({"message": "Forbidden"}), 403
            return f(*args, **kwargs)
        return decorated
    return wrapper
