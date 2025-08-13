# app/__init__.py
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template
from .config import DevelopmentConfig
from .extensions import db, migrate, jwt
from .resources.auth import auth_bp
from .resources.admin import admin_bp

def create_app(config_object=DevelopmentConfig):

    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_object)

    # initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register blueprints (Resources layer / Routes)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")


    @app.route("/")
    def landing():
        return render_template('landing.html')

    return app
