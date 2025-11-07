from flask import Blueprint

bp = Blueprint("api", __name__)  # ✅ 추가

from .auth import bp as auth_bp
bp.register_blueprint(auth_bp)     # 결과: /api/auth/*

from .posts import bp as posts_bp
bp.register_blueprint(posts_bp)    # 결과: /api/posts/*
