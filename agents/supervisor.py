from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain import hub
from dotenv import load_dotenv
import os

from agents.research_agent import build_research_agent
from agents.finance_agent import build_finance_agent
from agents.weather_agent import build_weather_agent
from utils.cost_tracker    import CostTracker

load_dotenv()

# Global tracker instance
tracker = CostTracker()

def safe_agent_call(agent: AgentExecutor, query: str, agent_name: str) -> str:
    """
    Wraps every specialist agent call with:
    - Error handling    → no crashes
    - Cost tracking     → counts LLM calls
    - Output validation → checks empty responses
    """
    try:
        tracker.add_call(tokens=600)  # estimate per specialist call
        result = agent.invoke({"input": query})
        output = result.get("output", "")

        # Output validation — catch empty or error responses
        if not output or len(output.strip()) < 5:
            return f"⚠️ {agent_name} returned an empty response. Please retry."

        return output

    except Exception as e:
        return f"⚠️ {agent_name} encountered an error: {str(e)}"

def build_supervisor() -> AgentExecutor:
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    # ── Build specialist agents ───────────────────────────────
    research_agent = build_research_agent()
    finance_agent  = build_finance_agent()
    weather_agent  = build_weather_agent()

    # ── Wrap each agent as a tool for supervisor ──────────────
    # This is the key pattern — agents become tools

    tools = [
        Tool(
            name="research_agent",
            func=lambda q: research_agent.invoke({"input": q})["output"],
            description="""Use this for searching news, facts, people, 
            companies, AI topics, salaries, or any general knowledge 
            questions that need current internet information."""
        ),
        Tool(
            name="finance_agent",
            func=lambda q: finance_agent.invoke({"input": q})["output"],
            description="""Use this for anything related to crypto prices,
            Bitcoin, Ethereum, financial calculations, or money math.
            Input should be the full financial question."""
        ),
        Tool(
            name="weather_agent",
            func=lambda q: weather_agent.invoke({"input": q})["output"],
            description="""Use this for weather information for any city.
            Input should be the city name or weather question."""
        ),
    ]

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=6,
        handle_parsing_errors=True
    )


def get_tracker() -> CostTracker:
    return tracker