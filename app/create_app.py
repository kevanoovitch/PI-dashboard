from flask import Flask


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from app import routes  # noqa: F401 - Import registers routes on the app.

    return app
