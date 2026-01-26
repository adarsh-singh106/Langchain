# Custom memory summary logic

from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

# --- THE STORE ---
# Currently: In-Memory (RAM). 
# Note: This resets every time you restart the server.
store = {}

def get_session_history(session_id: str):
    """
    Retrieves the chat history for a specific session ID.
    If it doesn't exist, it creates a new one.
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    
    return store[session_id]