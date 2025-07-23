# procurement_app/__init__.py
from flask import Flask, render_template
from .config import Config
from datetime import datetime
from .extensions import db, migrate
from flask_login import LoginManager

def create_app():
    app = Flask(__name__, static_folder='../static', instance_relative_config=True)
    app.config.from_object(Config)

    # Attempt to load the instance config.py if it exists
    try:
        app.config.from_pyfile('config.py', silent=True)
    except FileNotFoundError:
        pass # No instance config found, use defaults

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # The route to redirect to for login
    login_manager.init_app(app)

    from .models import User # Import here to avoid circular dependencies

    @app.context_processor
    def inject_now():
        """Inject the current datetime into templates."""
        return {'now': datetime.now()}

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints from your app
    from .main import main_bp
    app.register_blueprint(main_bp)
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .views import aie_bp
    app.register_blueprint(aie_bp)

    return app
