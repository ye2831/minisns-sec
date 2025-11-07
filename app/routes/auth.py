# app/routes/auth.py
from flask import Blueprint, request, jsonify
from .. import db
from ..models import User
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return {"msg": "username and password required"}, 400

    if User.query.filter_by(username=username).first():
        return {"msg": "user exists"}, 400

    u = User(username=username)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return {"msg": "registered", "user": u.to_dict()}, 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return {"msg": "username and password required"}, 400

    u = User.query.filter_by(username=username).first()
    if not u or not u.check_password(password):
        return {"msg": "bad username or password"}, 401

    access = create_access_token(
        identity=str(u.id),                # ✅ 문자열로
        expires_delta=timedelta(hours=1)
    )
    refresh = create_refresh_token(identity=str(u.id))
    return {
        "msg": "login successful",
        "access_token": access,
        "refresh_token": refresh,
        "user": u.to_dict()
    }, 200
