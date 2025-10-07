from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter

jwt = JWTManager()
hash = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
cors  = CORS()
mail = Mail()
# limiter = Limiter(key_func=lambda: "global")

'''Initialize all Extensions'''
def init_extensisons(app):
    jwt.init_app(app)
    hash.init_app(app)
    cors.init_app(app, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    # limiter.init_app(app)
    return None