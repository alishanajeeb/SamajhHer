from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """
    Binds SQLAlchemy to Flask and creates all tables.
    Called once when app starts.
    """
    db.init_app(app)
    with app.app_context():
        from models.user         import User
        from models.conversation  import Conversation
        from models.doctor_card   import DoctorCard
        db.create_all()
        print("SamajhHer database ready.")