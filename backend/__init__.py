from flask import Flask

from backend.routes import ALL_BLUEPRINTS


def create_app() -> Flask:
    app = Flask(__name__)
    for bp in ALL_BLUEPRINTS:
        app.register_blueprint(bp)
    return app
