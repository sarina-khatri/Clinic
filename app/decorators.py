# app/decorators.py
from functools import wraps
from flask import jsonify, session, redirect, url_for, flash, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def jwt_or_session_role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            try:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims.get("role") in allowed_roles:
                    return fn(*args, **kwargs)
            except Exception:
                pass

            # Try session role
            role = session.get('role')
            if role in allowed_roles:
                return fn(*args, **kwargs)

            # Unauthorized response
            if request.is_json or request.accept_mimetypes.accept_json:
                return jsonify({"msg": "Forbidden - insufficient role or missing auth"}), 403
            else:
                flash("You must be logged in with sufficient permissions", "error")
                return redirect(url_for("auth.login_page"))

        return wrapper
    return decorator
