from flask import Blueprint, current_app, jsonify, render_template, request

web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def index():
    return render_template("chat.html")


@web_bp.get("/health")
def health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@web_bp.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "message is required"}), 400

    rag_service = current_app.extensions["rag_service"]
    response = rag_service.ask(message)
    return jsonify(response), 200
