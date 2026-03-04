# Multi-Agent AI System

A production-style multi-agent AI system built with LangChain and Groq.
A Supervisor Agent intelligently routes queries to specialized agents.

## Architecture
```
User Query → Supervisor Agent → Research Agent  (web search)
                              → Finance Agent   (crypto + math)
                              → Weather Agent   (live weather)
```

## Features
- Real-time web search via Tavily
- Live crypto prices (BTC, ETH, SOL...)
- Real-time weather for any city
- Conversation memory across turns
- Cost & latency tracking per query
- Powered by Groq (ultra-fast inference)

## Tech Stack
| Layer | Technology |
|-------|-----------|
| LLM | Groq (llama3-70b-8192) |
| Framework | LangChain Agents |
| Search | Tavily Search API |
| Weather | Open-Meteo API |
| Crypto | CoinGecko API |
| UI | Streamlit |

## Performance
| Metric | Value |
|--------|-------|
| Avg response time | 3-6 seconds |
| LLM calls per query | 2-4 calls |
| Estimated cost per query | ~$0.001 |

## Roadmap
- [ ] Add email agent (read/summarize emails)
- [ ] Add memory persistence with ChromaDB
- [ ] Deploy to Railway with Docker
- [ ] Add authentication for multi-user support

## Setup
```bash
git clone https://github.com/YOUR_USERNAME/week3-ai-agent
cd week3-ai-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:
```
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

## Run
```bash
streamlit run app.py
```

## Example Queries
- "What are the latest AI trends in Europe?"
- "Get Bitcoin price and weather in Berlin"
- "AI engineer salaries in Netherlands 2025"