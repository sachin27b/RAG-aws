from flask import Flask
from app.config.settings import Settings
from app.config.logger import init_logger

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Settings.SECRET_KEY

    init_logger()

    from app.routes import kb_blueprint
    app.register_blueprint(kb_blueprint)

    return app
