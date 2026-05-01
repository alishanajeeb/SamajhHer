from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.conversation import Conversation
from services.gemini_service import get_ai_response
from services.prompt_service import get_welcome_message
from database import db

chat_bp = Blueprint("chat", __name__)

VALID_FLOWS     = ["woman", "family", "doctor"]
VALID_LANGUAGES = ["urdu", "roman_urdu", "english"]


@chat_bp.route("/start", methods=["POST"])
@jwt_required()
def start_conversation():
    """
    Starts a new conversation for a specific flow.
    Creates a DB record and returns the welcome message.
    Why save immediately? So history is preserved even if
    user closes app after first message.
    """
    user_id  = int(get_jwt_identity())
    data     = request.get_json()
    flow     = data.get("flow", "woman")
    language = data.get("language", "roman_urdu")

    if flow not in VALID_FLOWS:
        return jsonify({"error": "Invalid flow"}), 400
    if language not in VALID_LANGUAGES:
        return jsonify({"error": "Invalid language"}), 400

    # Get welcome message for this flow + language
    welcome = get_welcome_message(flow, language)

    # Create conversation record
    convo = Conversation(
        user_id=user_id,
        flow=flow,
        language=language,
        title=f"New {flow} conversation"
    )

    # Add welcome message to history
    convo.set_messages([{
        "role": "ai",
        "text": welcome
    }])

    db.session.add(convo)
    db.session.commit()

    return jsonify({
        "conversation_id": convo.id,
        "welcome_message": welcome,
        "flow":            flow,
        "language":        language
    }), 201


@chat_bp.route("/message", methods=["POST"])
@jwt_required()
def send_message():
    """
    Sends a user message and gets AI response.
    Steps:
    1. Load conversation history from DB
    2. Add user message to history
    3. Send to Gemini with full history
    4. Save AI response to DB
    5. Return AI response
    """
    user_id = int(get_jwt_identity())
    data    = request.get_json()

    convo_id     = data.get("conversation_id")
    user_message = data.get("message", "").strip()

    if not convo_id or not user_message:
        return jsonify({"error": "conversation_id and message are required"}), 400

    # Load conversation
    convo = Conversation.query.filter_by(
        id=convo_id, user_id=user_id
    ).first()

    if not convo:
        return jsonify({"error": "Conversation not found"}), 404

    # Get current history
    messages = convo.get_messages()

    # Add user message
    messages.append({"role": "user", "text": user_message})

    # Get AI response from Gemini
    ai_response = get_ai_response(
        flow=convo.flow,
        language=convo.language,
        messages=messages[:-1],  # history WITHOUT current message
        user_message=user_message
    )

    # Add AI response to history
    messages.append({"role": "ai", "text": ai_response})

    # Auto-generate title from first user message
    if convo.title == f"New {convo.flow} conversation":
        convo.title = user_message[:60] + ("..." if len(user_message) > 60 else "")

    # Save updated history
    convo.set_messages(messages)
    db.session.commit()

    return jsonify({
        "response":        ai_response,
        "conversation_id": convo.id
    }), 200


@chat_bp.route("/conversations", methods=["GET"])
@jwt_required()
def get_conversations():
    """Returns all conversations for logged-in user."""
    user_id = int(get_jwt_identity())
    flow    = request.args.get("flow")  # optional filter

    query = Conversation.query.filter_by(user_id=user_id)
    if flow:
        query = query.filter_by(flow=flow)

    convos = query.order_by(Conversation.updated_at.desc()).all()

    return jsonify({
        "conversations": [c.to_dict() for c in convos]
    }), 200


@chat_bp.route("/conversations/<int:convo_id>", methods=["GET"])
@jwt_required()
def get_conversation(convo_id):
    """Returns a single conversation with full message history."""
    user_id = int(get_jwt_identity())

    convo = Conversation.query.filter_by(
        id=convo_id, user_id=user_id
    ).first()

    if not convo:
        return jsonify({"error": "Conversation not found"}), 404

    return jsonify({"conversation": convo.to_dict()}), 200


@chat_bp.route("/conversations/<int:convo_id>", methods=["DELETE"])
@jwt_required()
def delete_conversation(convo_id):
    """Deletes a conversation."""
    user_id = int(get_jwt_identity())

    convo = Conversation.query.filter_by(
        id=convo_id, user_id=user_id
    ).first()

    if not convo:
        return jsonify({"error": "Conversation not found"}), 404

    db.session.delete(convo)
    db.session.commit()

    return jsonify({"message": "Conversation deleted"}), 200