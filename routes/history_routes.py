from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.conversation import Conversation
from models.doctor_card  import DoctorCard

history_bp = Blueprint("history", __name__)


@history_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_history():
    """
    Returns full history — all conversations and cards.
    Used on the history page to show everything in one place.
    """
    user_id = int(get_jwt_identity())

    convos = Conversation.query.filter_by(user_id=user_id)\
                               .order_by(Conversation.updated_at.desc())\
                               .all()

    cards  = DoctorCard.query.filter_by(user_id=user_id)\
                              .order_by(DoctorCard.created_at.desc())\
                              .all()

    return jsonify({
        "conversations": [c.to_dict() for c in convos],
        "doctor_cards":  [c.to_dict() for c in cards]
    }), 200