from flask import Flask, jsonify
from config import Config
from models import db
from routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return jsonify({"message": "Simple CRM API is running"})

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"error": "Method not allowed"}), 405

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
