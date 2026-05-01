from flask_jwt_extended import create_access_token
from models.user import User
from database import db


def get_bcrypt():
    from app import bcrypt
    return bcrypt


def register_user(name, email, password, language="roman_urdu"):
    existing = User.query.filter_by(email=email).first()
    if existing:
        return {"error": "Email already registered"}, 409

    bcrypt = get_bcrypt()
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        language=language
    )
    db.session.add(user)
    db.session.commit()

    return {"message": "Account created successfully", "user": user.to_dict()}, 201


def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "Invalid email or password"}, 401

    bcrypt = get_bcrypt()
    if not bcrypt.check_password_hash(user.password_hash, password):
        return {"error": "Invalid email or password"}, 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"language": user.language}
    )

    return {
        "message":      "Login successful",
        "access_token": token,
        "user":         user.to_dict()
    }, 200