from flask import Blueprint

bp = Blueprint("api", __name__)

from .auth import bp as auth_bp
bp.register_blueprint(auth_bp)
