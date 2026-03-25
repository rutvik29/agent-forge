"""Critic agent — reviews and approves outputs."""
from langchain_core.prompts import ChatPromptTemplate
from .base_agent import BaseAgent

SYSTEM = """You are a senior code reviewer. Evaluate the solution for:
1. Correctness - does it solve the problem?
2. Code quality - clean, typed, documented?
3. Edge cases - are they handled?

If all criteria pass, start your response with APPROVED.
Otherwise list specific improvements needed."""

class CriticAgent(BaseAgent):
    def __init__(self, llm_provider="openai", model="gpt-4o"):
        super().__init__("Critic", llm_provider, model)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM),
            ("human", "Query: {query}\nSolution:\n{code}\n\nReview:"),
        ])
        self.chain = self.prompt | self.llm

    def run(self, state):
        response = self.chain.invoke({"query": state["query"], "code": state.get("code","")})
        approved = "APPROVED" in response.content
        return {
            "critique": response.content,
            "final_answer": state.get("code") if approved else None,
            "next_agent": "end" if approved else "coder",
        }
