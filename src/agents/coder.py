"""Coder agent — writes and executes code."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.tools import PythonREPLTool
from .base_agent import BaseAgent

SYSTEM = """You are an expert Python engineer. Write clean, production-quality code with:
- Full type hints and docstrings
- Proper error handling
- Unit tests where applicable
Output only the code, no explanations."""

class CoderAgent(BaseAgent):
    def __init__(self, llm_provider="openai", model="gpt-4o"):
        super().__init__("Coder", llm_provider, model)
        self.repl = PythonREPLTool()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM),
            ("human", "Task: {query}\nResearch: {research}\nCritique: {critique}\n\nWrite the solution:"),
        ])
        self.chain = self.prompt | self.llm

    def run(self, state):
        research_str = "\n".join(state.get("research", []))
        response = self.chain.invoke({
            "query": state["query"], "research": research_str,
            "critique": state.get("critique", "None yet - first attempt"),
        })
        return {"code": response.content, "next_agent": "critic", "iteration": state.get("iteration",0)+1}
