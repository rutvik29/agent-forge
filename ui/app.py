"""Streamlit UI for Agent Forge."""
import streamlit as st
import httpx, json, asyncio

st.set_page_config(page_title="Agent Forge", page_icon="🤖", layout="wide")
st.title("🤖 Agent Forge")
st.caption("Multi-Agent Orchestration Framework")

with st.sidebar:
    st.header("⚙️ Configuration")
    provider = st.selectbox("LLM Provider", ["openai", "anthropic", "ollama"])
    model = st.text_input("Model", value="gpt-4o" if provider=="openai" else "claude-3-5-sonnet-20241022")
    max_iter = st.slider("Max Iterations", 1, 5, 3)
    api_url = st.text_input("API URL", value="http://localhost:8000")

col1, col2 = st.columns([2, 1])

with col1:
    query = st.text_area("Enter your query:", height=120,
        placeholder="e.g. Write a Python function to detect anomalies in time series data")

    if st.button("🚀 Run Agents", type="primary", disabled=not query):
        with st.spinner("Agents working..."):
            try:
                resp = httpx.post(f"{api_url}/query", json={
                    "query": query, "llm_provider": provider,
                    "model": model, "max_iterations": max_iter
                }, timeout=120)
                data = resp.json()
                st.success("✅ Task Complete!")
                st.code(data.get("result","No result"), language="python")
            except Exception as e:
                st.error(f"Error: {e}")

with col2:
    st.subheader("📊 Agent Flow")
    st.markdown("""
    1. **🧠 Planner** — Decomposes query
    2. **🔍 Researcher** — Gathers context  
    3. **💻 Coder** — Writes solution
    4. **🔎 Critic** — Reviews & approves
    """)
