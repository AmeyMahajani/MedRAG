from flask import Flask

from .services.rag import RAGService
from .web.routes import web_bp


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="web/templates",
        static_folder="web/static",
    )

    rag_service = RAGService()
    app.extensions["rag_service"] = rag_service
    app.register_blueprint(web_bp)

    return app
