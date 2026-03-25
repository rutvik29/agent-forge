"""Researcher agent — gathers information for tasks."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import TavilySearchResults
from .base_agent import BaseAgent

SYSTEM = """You are a thorough researcher. Given a task plan, gather all relevant information.
Use web search when needed. Return comprehensive, factual findings with sources."""

class ResearcherAgent(BaseAgent):
    def __init__(self, llm_provider="openai", model="gpt-4o"):
        super().__init__("Researcher", llm_provider, model)
        self.search_tool = TavilySearchResults(max_results=5)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM),
            ("human", "Plan: {plan}\nQuery: {query}\n\nResearch findings:"),
        ])
        self.chain = self.prompt | self.llm

    def run(self, state):
        response = self.chain.invoke({"plan": state.get("plan",""), "query": state["query"]})
        return {"research": [response.content], "next_agent": "coder"}
