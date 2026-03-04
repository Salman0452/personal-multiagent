import streamlit as st
from agents.supervisor import build_supervisor, get_tracker

st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="centered"
)

# ── Header ────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Multi-Agent AI System")
    st.caption("Supervisor routes queries to specialized AI agents")

with col2:
    st.markdown("### Agents Online")
    st.success("Research Agent")
    st.success("Finance Agent")
    st.success("Weather Agent")

st.divider()

# ── Session State ─────────────────────────────────────────────
if "agent" not in st.session_state:
    with st.spinner("Initializing all agents..."):
        st.session_state.agent    = build_supervisor()
        st.session_state.messages = []
        st.session_state.stats    = []


# ── Chat History ──────────────────────────────────────────────
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show stats under assistant messages
        if message["role"] == "assistant" and i // 2 < len(st.session_state.stats):
            stat = st.session_state.stats[i // 2]
            st.caption(
                f"{stat['elapsed_seconds']}s  •  "
                f"{stat['llm_calls']} LLM calls  •  "
                f"~${stat['estimated_cost']} estimated cost"
            )

# ── Chat Input ────────────────────────────────────────────────
if prompt := st.chat_input("Ask anything — weather, crypto, news..."):

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Supervisor routing your query..."):
            tracker = get_tracker()
            tracker.start()

            try:
                response = st.session_state.agent.invoke({"input": prompt})
                answer   = response["output"]
            except Exception as e:
                answer = f"System error: {str(e)}"

            tracker.stop()
            stats = tracker.get_summary()

        st.markdown(answer)
        st.caption(
            f"{stats['elapsed_seconds']}s  •  "
            f"{stats['llm_calls']} LLM calls  •  "
            f"~${stats['estimated_cost']} estimated cost"
        )

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.stats.append(stats)


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("🏗️ Architecture")
    st.markdown("""
```
    User Query
        ↓
    Supervisor Agent
        ↓
    ┌───────────────┐
    │ Research Agent│ → Web Search
    │ Finance Agent │ → Crypto + Math
    │ Weather Agent │ → Live Weather
    └───────────────┘
```
    """)


    st.divider()
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.stats    = []
        st.session_state.agent    = build_supervisor()
        st.rerun()

    st.divider()
    st.caption("Week 3 — AI Agents Bootcamp\nBuilt with LangChain + Groq")