from database import db
from datetime import datetime


class DoctorCard(db.Model):
    __tablename__ = "doctor_cards"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Raw symptoms the user entered
    symptoms   = db.Column(db.Text, nullable=False)

    # Duration of symptoms
    duration   = db.Column(db.String(100), nullable=True)

    # Severity — mild / moderate / severe
    severity   = db.Column(db.String(50), nullable=True)

    # AI-generated structured card content in chosen language
    card_content = db.Column(db.Text, nullable=False)

    # Language of this card
    language   = db.Column(db.String(20), nullable=False, default="urdu")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="doctor_cards")

    def to_dict(self):
        return {
            "id":           self.id,
            "symptoms":     self.symptoms,
            "duration":     self.duration,
            "severity":     self.severity,
            "card_content": self.card_content,
            "language":     self.language,
            "created_at":   self.created_at.isoformat()
        }