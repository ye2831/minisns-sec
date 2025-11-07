from flask import Blueprint, request, jsonify, render_template, current_app, abort
from .. import db
from ..models import Post, User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("posts", __name__)

@bp.route("/posts", methods=["GET"])
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).limit(50).all()
    return jsonify([p.to_dict() for p in posts]), 200

@bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json() or {}
    title = data.get("title")
    content = data.get("content")
    allow_html = bool(data.get("allow_html", False))
    if not title or not content:
        return {"msg":"title and content required"}, 400
    identity = get_jwt_identity()
    user_id = identity.get("id")
    p = Post(user_id=user_id, title=title, content=content, allow_html=allow_html)
    db.session.add(p)
    db.session.commit()
    return {"msg":"created","post":p.to_dict()}, 201

@bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    p = Post.query.get_or_404(post_id)
    # If in vulnerable mode and allow_html True, render raw HTML (Stored XSS demo)
    if current_app.config.get("VULNERABLE_MODE") and p.allow_html:
        # render template that outputs content without escaping
        return render_template("post_detail_vuln.html", post=p)
    # safe render
    return render_template("post_detail.html", post=p)
