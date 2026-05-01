from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name     = data.get("name", "").strip()
    email    = data.get("email", "").strip()
    password = data.get("password", "").strip()
    language = data.get("language", "roman_urdu")

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    res, code = register_user(name, email, password, language)
    return jsonify(res), code


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    email    = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    res, code = login_user(email, password)
    return jsonify(res), code