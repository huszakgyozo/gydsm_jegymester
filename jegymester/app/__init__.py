from pyexpat.errors import messages
from flask import Flask, request
from sqlalchemy.sql.functions import current_user
from config import Config
from apiflask import APIFlask
from config import Config
from app.extensions import db
from app.routes.auth import verify_token
from app.models import *

def create_app(config_class=Config):
    # API-k kiprobalasa ha nem kell
    #app = Flask(__name__)

    # API-k kiprobalasahoz
    app = APIFlask(__name__, json_errors=True,
                   title="Jegymester API",
                   docs_path="/swagger")
                    
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    from flask_migrate import Migrate
    migrate = Migrate(app, db, render_as_batch=True)

    # Register blueprints here
    from app.blueprints import bp as bp_default
    app.register_blueprint(bp_default, url_prefix='/api')

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    @app.context_processor
    def inject_user():
        return dict(current_user=verify_token(""))

    return app