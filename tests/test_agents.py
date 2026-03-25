"""Tests for Agent Forge."""
import pytest
from unittest.mock import MagicMock, patch
from src.agents.base_agent import BaseAgent
from src.orchestrator.graph import build_agent_graph, AgentState

class ConcreteAgent(BaseAgent):
    def run(self, state):
        return {"plan": "test plan"}

@pytest.fixture
def mock_agent():
    with patch("src.agents.base_agent.ChatOpenAI") as mock_llm:
        mock_llm.return_value = MagicMock()
        agent = ConcreteAgent("Test", "openai", "gpt-4o")
        return agent

def test_agent_initialization(mock_agent):
    assert mock_agent.name == "Test"

def test_agent_run(mock_agent):
    state = {"query": "test", "iteration": 0, "max_iterations": 3, "research": []}
    result = mock_agent.run(state)
    assert "plan" in result
