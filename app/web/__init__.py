from flask import Flask


def create_app():

    app = Flask(
        __name__,
        template_folder="../../dashboard/templates",
        static_folder="../../dashboard/static"
    )

    from app.web.routes import main
    from app.web.api import api

    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix="/api")

    return app