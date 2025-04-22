from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register the blueprint
    from .routes import main
    app.register_blueprint(main)

    # Pass data if needed (e.g., configuration, extensions)
    return app