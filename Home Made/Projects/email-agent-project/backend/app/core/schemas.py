# Pydantic models (EmailDraft, etc.)

from pydantic import BaseModel, Field
from typing import Union, Literal, Optional



# 1. EMAIL DRAFT (The Action)
class EmailDraft(BaseModel):
    """The final structure of the email to be generated."""
    # response_type is CRITICAL. It tells the code "This is an email" automatically.
    response_type: Literal["email_draft", "EmailDraft"] = Field(default="email_draft")
    
    subject_line: str = Field(description="A catchy, professional subject line")
    body: str = Field(description="The main content of the email, formatted with newlines")
    recipient_category: Literal["Professional", "Personal", "Unknown"]
    
    # Meta-Data
    intent: str = Field(description="The primary goal (e.g., 'Requesting Leave')")
    tone: str = Field(description="e.g., 'Empathetic', 'Assertive'")
    urgency_level: Literal["Low", "Medium", "High"]
    
    # Analysis
    tone_analysis: str = Field(description="Why this tone was chosen") 

# 2. CLARIFICATION (The Guardrail)
class ClarificationQuestion(BaseModel):
    """Used when the request is vague."""
    response_type: Literal["ask_for_info", "ClarificationQuestion"] = Field(default="ask_for_info")
    
    missing_info: str = Field(description="What specific info is missing?")
    question_to_user: str = Field(description="Polite question to ask the user.")

# 3. GENERAL CHAT (The Fallback)
class GeneralChat(BaseModel):
    """Standard conversational response."""
    response_type: Literal["general_chat", "GeneralChat"] = Field(default="general_chat")
    
    answer: str = Field(description="Conversational reply.")


# # 4. SAVE INFO ABOUT USER (LEARNER)
# class SaveUserFact(BaseModel):
#     """
#     Call this tool silently when the user mentions a permanent fact about themselves.
#     """
#     response_type: Literal["save_fact"] = Field(default="save_fact")

#     fact_category: Literal["name", "job_title", "location", "preference"]
#     fact_value: str = Field(description="The value to save, e.g., 'John' or 'NYC'")

# # 5. SAVE INFO ABOUT THE PAST EMAIL USER SENTS
# class SaveEmailFact(BaseModel):
#     """
#     call this tool silently when user enter an actual email address and ask for Email Draft
#     also if the user mentions multiple people at the same time run this multiple time 
#     """
#     response_type: Literal["save_email_fact"] =Field(default="save_email_fact")

#     reciver_category:Literal["family_member","friend",'wife/girlfriend',"comapany","profesional"]
#     reciver_email: str = Field(description="The exact email adderess of the reciver email")
#     email_intent:str = Field(description="What was the intension of writing the email")
#     extra_helpful_info:str|None = Field(description="The info that might be relevant or worth remmbering")







# Gemini (Google GenAI) integration in LangChain does not yet 
# support passing a raw Union (like Union[Email, Chat])

class AgentResponse(BaseModel):
    """
    Wrapper class to help the LLM pick the right output type.
    This works around the 'UnionGenericAlias' error in Gemini.
    """
    final_output: Union[EmailDraft, ClarificationQuestion, GeneralChat]