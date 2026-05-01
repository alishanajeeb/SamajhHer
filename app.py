from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config
from database import init_db

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    bcrypt.init_app(app)
    JWTManager(app)

    # Database
    init_db(app)

    # ── API Blueprints ────────────────────────────────────────────────────
    from routes.auth_routes    import auth_bp
    from routes.chat_routes    import chat_bp
    from routes.card_routes    import card_bp
    from routes.history_routes import history_bp

    app.register_blueprint(auth_bp,     url_prefix="/api/auth")
    app.register_blueprint(chat_bp,     url_prefix="/api/chat")
    app.register_blueprint(card_bp,     url_prefix="/api/card")
    app.register_blueprint(history_bp,  url_prefix="/api/history")

    # ── Page Routes ───────────────────────────────────────────────────────
    @app.route("/")
    def landing():
        return render_template("landing.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/register")
    def register_page():
        return render_template("register.html")

    @app.route("/woman")
    def woman_page():
        return render_template("woman_flow.html")

    @app.route("/family")
    def family_page():
        return render_template("family_flow.html")

    @app.route("/doctor")
    def doctor_page():
        return render_template("doctor_flow.html")

    @app.route("/history")
    def history_page():
        return render_template("history.html")

    @app.route("/card/<int:card_id>")
    def card_print_page(card_id):
        return render_template("doctor_card.html", card_id=card_id)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)