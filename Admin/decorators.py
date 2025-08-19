# app/Admin/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

def jwt_role_required(allowed_roles):
    def outer(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt() or {}
            role = claims.get("role")
            if role not in allowed_roles:
                return jsonify({"msg": "Forbidden - insufficient role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return outer
