from dotenv import load_dotenv
load_dotenv()  
from flask import Flask
from flask_jwt_extended import JWTManager
from app.config.database import db,ma
from app.config.config import Config
from app.auth.auth_routes import auth_bp
from app.admin.admin_routes import admin_bp
from app.doctor_availability.availablity_routes import availability_bp
from app.appointment.appointment_routes import appointment_bp
from app.reimbursement.reimbursement_routes import reimbursement_bp


def create_app():
    

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(availability_bp, url_prefix="/availability")
    app.register_blueprint(appointment_bp, url_prefix="/appointments")
    app.register_blueprint(reimbursement_bp, url_prefix="/reimbursement")

    return app

