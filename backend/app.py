"""ReviewGuard backend entrypoint."""

from flask import Flask
from flask_cors import CORS

from config import Config
from routes.moderation_routes import moderation_bp
from utils.response_utils import error_response


def create_app():
    """Application factory for the ReviewGuard Flask app."""
    Config.validate()

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(moderation_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return error_response("Resource not found.", status_code=404)

    @app.errorhandler(500)
    def server_error(_error):
        return error_response("Internal server error.", status_code=500)

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=Config.FLASK_DEBUG, port=5000)