from database import db
from datetime import datetime
import json


class Conversation(db.Model):
    __tablename__ = "conversations"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Which of the 3 flows this conversation belongs to
    # Values: "woman" | "family" | "doctor"
    flow       = db.Column(db.String(20), nullable=False)

    # Language used in this conversation
    language   = db.Column(db.String(20), nullable=False, default="roman_urdu")

    # Full message history stored as JSON string
    # Format: [{"role": "user", "text": "..."}, {"role": "ai", "text": "..."}]
    messages   = db.Column(db.Text, nullable=False, default="[]")

    # Short title auto-generated from first message
    title      = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="conversations")

    def get_messages(self):
        """Returns messages as Python list."""
        return json.loads(self.messages)

    def set_messages(self, messages_list):
        """Saves messages list as JSON string."""
        self.messages = json.dumps(messages_list, ensure_ascii=False)

    def to_dict(self):
        return {
            "id":         self.id,
            "flow":       self.flow,
            "language":   self.language,
            "title":      self.title,
            "messages":   self.get_messages(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }