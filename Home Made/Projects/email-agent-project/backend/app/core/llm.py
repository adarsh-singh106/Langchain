# LLM initialization logic (Groq/Gemini)


import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load Env variables (Safe for Render & Local)
load_dotenv()

def get_llm(model_name: str = "gemini-3-flash-preview", provider: str = "google_genai",temperature: float = 0):
    """
    Factory function to return the requested LLM.
    
    Args:
        model_name (str): The specific model ID (e.g., 'llama-3.3-70b-versatile').
        provider (str): The provider key (e.g., 'groq', 'google_genai', 'openai').
    
    Returns:
        BaseChatModel: The initialized LangChain chat model.
    """
    
    # 1. Check for keys 
    if provider == "google_genai" and not os.getenv("GEMINI_API_KEY"):
        raise ValueError("CRITICAL: GEMINI_API_KEY is missing from environment variables.")
    
    if provider == "groq" and not os.getenv("GROQ_API_KEY"):
        raise ValueError("CRITICAL: GROQ_API_KEY is missing from environment variables.")

    try:
        # 2. Initialize the model
        llm = init_chat_model(
            model=model_name,
            model_provider=provider,
            temperature=temperature  # let the caller decide
        )
        
        # 3. RETURN the model 
        return llm
        
    except Exception as e:
        # 4. Show the ACTUAL error message if something breaks
        raise RuntimeError(f"Failed to initialize LLM: {str(e)}")