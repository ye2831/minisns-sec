from flask import Blueprint, request, jsonify, current_app
from ..models import User
from .. import db
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return {"msg":"username and password required"}, 400
    if User.query.filter_by(username=username).first():
        return {"msg":"user exists"}, 400
    u = User(username=username)
    u.set_password(password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"msg":"user exists or db error"}, 400
    return {"msg":"registered","user":u.to_dict()}, 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return {"msg":"username/password required"}, 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {"msg":"invalid credentials"}, 401
    access = create_access_token(identity={"id": user.id, "username": user.username, "is_admin": user.is_admin})
    return {"access_token": access}, 200
