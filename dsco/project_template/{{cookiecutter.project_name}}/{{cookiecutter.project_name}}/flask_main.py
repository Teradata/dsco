from flask import Flask, g
from . import dashapp1


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    dashapp1.add_dash(app)
    #app.config.from_object('config.Config')

    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        app.register_blueprint(routes.main_bp)

        return app
