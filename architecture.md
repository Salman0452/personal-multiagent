# System Architecture

## Agent Flow
\```
User Input
    ↓
Streamlit UI (app.py)
    ↓
Supervisor Agent (agents/supervisor.py)
    ↓
┌─────────────────────────────────────┐
│                                     │
▼                 ▼                   ▼
Research Agent    Finance Agent    Weather Agent
(Tavily Search)  (CoinGecko API)  (Open-Meteo API)
                 (Calculator)
└─────────────────────────────────────┘
    ↓
Cost Tracker (utils/cost_tracker.py)
    ↓
Final Answer → Streamlit UI
\```

## Key Design Decisions

**Why Multi-Agent over Single Agent?**
One agent with many tools causes hallucination and wrong
tool selection. Specialized agents with fewer tools each
are more reliable and scalable.

**Why Groq?**
Agents make multiple LLM calls per query. Groq's
ultra-fast inference reduces latency significantly
compared to standard OpenAI endpoints.

**Why Tavily over DuckDuckGo?**
Tavily is purpose-built for AI agents — returns
structured, clean results with better reliability
and rate limits.

## File Structure
\```
├── tools/          # Reusable tool functions
├── agents/         # Specialist + supervisor agents  
├── utils/          # Cost tracking, helpers
└── app.py          # Streamlit UI entry point
\```