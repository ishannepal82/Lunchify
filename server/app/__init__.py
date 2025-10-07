from flask import Flask
from .extensions import init_extensisons
from config import Config
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    init_extensisons(app)

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app
