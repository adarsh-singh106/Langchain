# Flask routes (Blueprints) go here

# backend/app/api/routes.py
from flask import Blueprint, request, Response, stream_with_context
from app.services.workflow import process_chat_stream # <--- Import the new function

api_bp = Blueprint('api', __name__)

@api_bp.route('/chat/stream', methods=['POST']) # <--- Changed URL to /stream (optional)
def chat_stream_endpoint():
    data = request.json
    user_input = data.get('message')
    session_id = data.get('session_id', 'default')

    if not user_input:
        return {"error": "No message"}, 400

    # 1. Create the Generator
    def generate():
        # We assume the generator yields JSON strings with newlines
        for chunk in process_chat_stream(user_input, session_id):
            yield chunk

    # 2. Return a 'Response' object with direct pass-through
    return Response(stream_with_context(generate()), mimetype='application/x-ndjson')