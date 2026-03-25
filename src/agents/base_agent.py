"""Base agent class with LLM-agnostic interface."""
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    SUPPORTED_PROVIDERS = {"openai", "anthropic", "ollama"}
    
    def __init__(self, name, llm_provider="openai", model="gpt-4o", temperature=0.1):
        self.name = name
        self.llm = self._init_llm(llm_provider, model, temperature)
    
    def _init_llm(self, provider, model, temperature):
        if provider == "openai":
            return ChatOpenAI(model=model, temperature=temperature, streaming=True)
        elif provider == "anthropic":
            return ChatAnthropic(model=model, temperature=temperature)
        elif provider == "ollama":
            return Ollama(model=model)
        raise ValueError(f"Unsupported: {provider}")
    
    @abstractmethod
    def run(self, state: dict) -> dict:
        pass
