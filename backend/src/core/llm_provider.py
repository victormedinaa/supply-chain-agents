"""
LLM Provider Factory.

Handles the creation of LLM instances, automatically falling back to a 
sophisticated Mock implementation if OpenAI credentials are unavailable.
This ensures the simulation can run offline or in CI/CD environments.
"""

import os
from typing import Any
from langchain_openai import ChatOpenAI
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.language_models import BaseChatModel

class RealisticMockChat(BaseChatModel):
    """
    A Mock Chat Model that returns semi-realistic responses based on keywords 
    in the prompt, rather than just random text.
    """
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        last_msg = messages[-1].content
        response = ""
        
        if "forecast" in last_msg.lower():
            response = '{"SKU-00001": 500, "SKU-00002": 120}' # JSON for forecaster
        elif "negotiation" in last_msg.lower():
            response = "Dear Supplier,\n\nGiven the high risk score of 0.85, we require immediate confirmation of expedited shipping.\n\nSincerely,\nProcurement"
        else:
            response = "Simulated thought process based on internal heuristics."
            
        gen = ChatGeneration(message=AIMessage(content=response))
        return ChatResult(generations=[gen])

    @property
    def _llm_type(self) -> str:
        return "realistic-mock"

def get_llm(model_name: str = "gpt-4-turbo", temperature: float = 0.7) -> BaseChatModel:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return ChatOpenAI(model=model_name, temperature=temperature)
    else:
        print(f"([SYSTEM] NOTICE: OpenAI API Key not found. Using Mock LLM for {model_name})")
        return RealisticMockChat()
