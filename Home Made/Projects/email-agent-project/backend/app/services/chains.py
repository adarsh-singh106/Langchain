# LangChain Runnable definitions
# Goal: Create a runnable object that takes input and gives structured output.

from app.core.llm import get_llm
from app.core.prompts import prompt
from app.core.schemas import EmailDraft, ClarificationQuestion, GeneralChat
from typing import Union
from app.core.schemas import AgentResponse

# 1. Get the Model
llm = get_llm(temperature=0) # Low temp for strict adherence to schemas

# 2. Bind the Schemas (The "Tools")
# This tells the LLM: "You MUST output one of these 3 JSON structures"
structured_llm = llm.with_structured_output(AgentResponse)

# 3. Create the Chain
# Input (Dict) -> Prompt -> LLM -> JSON Object
main_chain = prompt | structured_llm


