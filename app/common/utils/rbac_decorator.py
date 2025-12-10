from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from flask import  jsonify


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
