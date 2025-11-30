from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import DevelopmentConfig

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)

    from .routes.port_routes import port_bp
    app.register_blueprint(port_bp, url_prefix='/api')

    return app
