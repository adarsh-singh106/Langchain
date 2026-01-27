# The main Router -> Enhancer -> Writer logic

# backend/app/services/workflow.py
import json
from app.services.chains import main_chain
from app.core.memory import get_session_history

def process_chat_stream(user_input: str, session_id: str):
    """
    Generator function that streams updates to the client.
    """
    history_obj = get_session_history(session_id)
    chat_history = history_obj.messages

    # 1. Notify Client: We are starting
    # We yield a JSON string followed by a newline (standard SSE format)
    yield json.dumps({"step": "thinking", "message": "🧠 Analyzing your request..."}) + "\n"

    # 2. Run the Chain
    # (Note: 'main_chain' takes a few seconds, so the user sees the 'Thinking' message while waiting)
    wrapper_result = main_chain.invoke({
        "user_input": user_input,
        "chat_history": chat_history
    })
    
    # 3. Notify Client: We are done logic, processing output
    yield json.dumps({"step": "processing", "message": "✅ Response generated..."}) + "\n"

    # 4. Unpack & Save Memory
    response = wrapper_result.final_output
    
    history_obj.add_user_message(user_input)
    if hasattr(response, 'body'):
        ai_text = f"Drafted email: {response.subject_line}\n{response.body}"
    elif hasattr(response, 'question_to_user'):
        ai_text = response.question_to_user
    else:
        ai_text = response.answer
    history_obj.add_ai_message(ai_text)

    # 5. Yield the FINAL Result
    # We allow the frontend to distinguish between a 'status update' and the 'final data'
    final_payload = {
        "step": "done",
        "payload": response.model_dump()
    }
    yield json.dumps(final_payload) + "\n"