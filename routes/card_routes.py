from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.doctor_card import DoctorCard
from services.gemini_service import generate_doctor_card_content
from database import db

card_bp = Blueprint("card", __name__)


@card_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate_card():
    """
    Generates a structured doctor visit card.
    Saves it to DB so user can access it later.
    """
    user_id  = int(get_jwt_identity())
    data     = request.get_json()

    symptoms = data.get("symptoms", "").strip()
    duration = data.get("duration", "").strip()
    severity = data.get("severity", "moderate")
    language = data.get("language", "roman_urdu")

    if not symptoms:
        return jsonify({"error": "Symptoms are required"}), 400

    # Generate card content via Gemini
    card_content = generate_doctor_card_content(
        symptoms, duration, severity, language
    )

    # Save to database
    card = DoctorCard(
        user_id=user_id,
        symptoms=symptoms,
        duration=duration,
        severity=severity,
        card_content=card_content,
        language=language
    )
    db.session.add(card)
    db.session.commit()

    return jsonify({
        "card_id":      card.id,
        "card_content": card_content
    }), 201


@card_bp.route("/my-cards", methods=["GET"])
@jwt_required()
def get_my_cards():
    """Returns all saved doctor cards for logged-in user."""
    user_id = int(get_jwt_identity())

    cards = DoctorCard.query.filter_by(user_id=user_id)\
                            .order_by(DoctorCard.created_at.desc())\
                            .all()

    return jsonify({
        "cards": [c.to_dict() for c in cards]
    }), 200


@card_bp.route("/<int:card_id>", methods=["GET"])
@jwt_required()
def get_card(card_id):
    """Returns a single doctor card for printing."""
    user_id = int(get_jwt_identity())

    card = DoctorCard.query.filter_by(
        id=card_id, user_id=user_id
    ).first()

    if not card:
        return jsonify({"error": "Card not found"}), 404

    return jsonify({"card": card.to_dict()}), 200