from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from flask import  jsonify
from app.common.utils.feature_flags import FEATURE_FLAGS


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

def feature_flag_required(flag_name: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not FEATURE_FLAGS.get(flag_name, False):
                return jsonify({
                    "error": f"Feature '{flag_name}' is currently disabled"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

