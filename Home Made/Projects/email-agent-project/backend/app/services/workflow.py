# The main Router -> Enhancer -> Writer logic
from app.services.chains import main_chain
from app.core.memory import get_session_history
from langchain_core.messages import HumanMessage, AIMessage

def process_chat(user_input: str, session_id: str):
    # 1. Fetch History
    history_obj = get_session_history(session_id)
    chat_history = history_obj.messages

    # 2. Run the Chain
    # We pass 'chat_history' so the LLM remembers previous context
    response = main_chain.invoke({
        "user_input": user_input,
        "chat_history": chat_history
    })

    # 3. Save to Memory
    # Add User's input
    history_obj.add_user_message(user_input)
    
    # Add AI's response (We convert the object back to a string for storage)
    if hasattr(response, 'body'): # It's an EmailDraft
        ai_text = f"Drafted email: {response.subject_line}\n{response.body}"
    elif hasattr(response, 'question_to_user'): # It's a Clarification
        ai_text = response.question_to_user
    else: # It's General Chat
        ai_text = response.answer
        
    history_obj.add_ai_message(ai_text)

    # 4. Return the Raw JSON Object to Frontend
    # React frontend will decide how to render it based on 'response_type'
    return response.model_dump()