# procurement_app/__init__.py
from flask import Flask, render_template
from .config import Config

def create_app():
    app = Flask(__name__, static_folder='../static', instance_relative_config=True)
    app.config.from_object(Config)

    # Attempt to load the instance config.py if it exists
    try:
        app.config.from_pyfile('config.py', silent=True)
    except FileNotFoundError:
        pass # No instance config found, use default from .config.py

    # Initialize extensions here if you have them (e.g., db, login_manager)
    # from .extensions import db, login_manager
    # db.init_app(app)
    # login_manager.init_app(app)

    # Register blueprints
    from .views import app_bp
    app.register_blueprint(app_bp)

    # Add a simple route for the root URL
    @app.route('/')
    def index():
        return "Welcome to the Procurement App! Try navigating to /aie/new"

    return app