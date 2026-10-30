
from flask import Flask
from config import Config
from app.extensions import db, migrate, bcrypt
from app.routes import main


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from app import models

    from app.auth import auth
    from app.usuarios import usuarios
    from app.categorias import categorias
    from app.anuncios import anuncios

    app.register_blueprint(auth)
    app.register_blueprint(usuarios)
    app.register_blueprint(categorias)
    app.register_blueprint(anuncios)
    app.register_blueprint(main)

    return app
