from flask import Blueprint

admin_bp = Blueprint("admin", __name__)

@admin_bp.get("/")
def admin_root():
    return {"message": "admin works"}

