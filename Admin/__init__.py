# app/Admin/__init__.py
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from config import DevelopmentConfig
from extensions import db, migrate, jwt
from common.auth import auth_bp
from Admin.routes import admin_bp
from Appointment.routes import appointment_bp
from Doctor.routes import doctor_bp
from Doctor.models import DoctorAvailability
from Appointment.models import Appointment


def create_app(config_object=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(appointment_bp, url_prefix="/appointments")
    app.register_blueprint(doctor_bp, url_prefix="/doctor")

    return app
