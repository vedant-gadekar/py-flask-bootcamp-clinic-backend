from flask import Flask
from flask_jwt_extended import JWTManager
from app.config.db import db,ma
from app.config.config import Config
from app.auth.auth_routes import auth_bp
from app.admin.admin_routes import admin_bp


def create_app():
    from dotenv import load_dotenv
    from pathlib import Path

    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)

    JWTManager(app)

    
    with app.app_context():
        db.create_all()
        
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return "API is running", 200
    
    return app
    
    