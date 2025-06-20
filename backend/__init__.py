from flask import Flask

from backend.routes import base_bp, damage_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(base_bp)
    app.register_blueprint(damage_bp)
    return app
