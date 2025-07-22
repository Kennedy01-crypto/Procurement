# procurement_app/__init__.py
from flask import Flask, render_template
from .config import Config
from datetime import datetime

def create_app():
    app = Flask(__name__, static_folder='../static', instance_relative_config=True)
    app.config.from_object(Config)

    # Attempt to load the instance config.py if it exists
    try:
        app.config.from_pyfile('config.py', silent=True)
    except FileNotFoundError:
        pass # No instance config found, use default from .config.py

    # Initialize Flask-Login
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)

    @app.context_processor
    def inject_now():
        """Inject the current datetime into templates."""
        return {'now': datetime.now()}

    # Placeholder user_loader (replace with your actual user model logic)
    @login_manager.user_loader
    def load_user(user_id):
        return None  # Replace with: return User.query.get(int(user_id))

    # Register blueprints
    from .views import app_bp
    app.register_blueprint(app_bp)

    # Add a simple route for the root URL
    @app.route('/')
    def index():
        return "Welcome to the Procurement App! Try navigating to /aie/new or /aie/list"

    return app