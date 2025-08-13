# app/resources/auth.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from ..schemas import RegisterSchema, LoginSchema
from ..services import AuthService

auth_bp = Blueprint("auth", __name__)

#register
@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    if request.is_json:
        payload = request.get_json()
    else:
        payload = request.form.to_dict()

    schema = RegisterSchema()
    errors = schema.validate(payload)
    if errors:
        if request.is_json:
            return jsonify(errors), 400
        else:
            for field, err_msgs in errors.items():
                for msg in err_msgs:
                    flash(f"{field}: {msg}", "error")
            return redirect(url_for("auth.register_page"))

    username = payload["username"]
    email = payload["email"]
    password = payload["password"]
    role = payload["role"]

    if role == "admin":
        msg = "Cannot self-register as admin"
        if request.is_json:
            return jsonify({"msg": msg}), 403
        else:
            flash(msg, "error")
            return redirect(url_for("auth.register_page"))

    try:
        user = AuthService.register_user(username, email, password, role)
    except ValueError as e:
        msg = str(e)
        if request.is_json:
            return jsonify({"msg": msg}), 400
        else:
            flash(msg, "error")
            return redirect(url_for("auth.register_page"))

    additional_claims = {"role": user.role, "username": user.username}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)

    if not request.is_json:
        session['username'] = user.username
        session['role'] = user.role
        return redirect(url_for("auth.dashboard", token=access_token))

    return jsonify({
        "access_token": access_token,
        "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
    }), 201

# login
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# login POST
@auth_bp.route("/login", methods=["POST"])
def login():
    if request.is_json:
        payload = request.get_json()
    else:
        payload = request.form.to_dict()

    schema = LoginSchema()
    errors = schema.validate(payload)
    if errors:
        if request.is_json:
            return jsonify(errors), 400
        else:
            for field, err_msgs in errors.items():
                for msg in err_msgs:
                    flash(f"{field}: {msg}", "error")
            return redirect(url_for("auth.login_page"))

    username = payload["username"]
    password = payload["password"]

    user = AuthService.authenticate(username, password)
    if not user:
        msg = "Invalid username or password"
        if request.is_json:
            return jsonify({"msg": msg}), 401
        else:
            flash(msg, "error")
            return redirect(url_for("auth.login_page"))

    session['username'] = user.username
    session['role'] = user.role

    additional_claims = {"role": user.role, "username": user.username}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)

    if not request.is_json:
        return redirect(url_for("auth.dashboard", token=access_token))

    return jsonify({
        "access_token": access_token,
        "user": {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
    }), 200

@auth_bp.route("/dashboard", methods=["GET"])
@jwt_required(optional=True)
def dashboard():
    username = session.get('username')
    role = session.get('role')
    return render_template('dashboard.html', username=username, role=role)

@auth_bp.route("/logout")
def logout():
    session.clear()
    print("Logged out!!")
    flash("Logged out successfully", "success")
    return redirect(url_for("auth.login_page"))
