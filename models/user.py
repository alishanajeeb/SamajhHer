from database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Language preference — stored so UI auto-switches on login
    # Values: "urdu" | "roman_urdu" | "english"
    language      = db.Column(db.String(20), nullable=False, default="roman_urdu")

    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    conversations = db.relationship("Conversation", back_populates="user",
                                     lazy=True, cascade="all, delete-orphan")
    doctor_cards  = db.relationship("DoctorCard",   back_populates="user",
                                     lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id":       self.id,
            "name":     self.name,
            "email":    self.email,
            "language": self.language
        }