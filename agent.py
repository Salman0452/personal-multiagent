from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.memory import ConversationBufferMemory
from langchain import hub
from dotenv import load_dotenv
import os

# Import your custom tools
from tools.weather import get_weather
from tools.crypto import get_crypto_price
from tools.summarizer import summarize_text

load_dotenv()

# ── 1. LLM ──────────────────────────────────────────────────
def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

# ── 2. Tools ─────────────────────────────────────────────────
def get_tools():
    # Tavily is purpose-built for AI agents — much more reliable
    search_tool = TavilySearchResults(
        api_key=os.getenv("TAVILY_API_KEY"),
        max_results=3
    )

    def calculator(expression: str) -> str:
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Error: {str(e)}"

    return [
        Tool(
            name="web_search",
            func=search_tool.run,
            description="""ALWAYS use this tool to search for any salary,
            price, news, or real world data. Never rely on your training 
            data for facts. Input should be a specific search query string."""
        ),
        Tool(
            name="calculator",
            func=calculator,
            description="""ALWAYS use this tool for ANY mathematical 
            calculation no matter how simple. Never do math in your head.
            Input must be a valid Python math expression like '100000 / 12'."""
        ),
        # ── Custom tools plugged in here ──
        get_weather,
        get_crypto_price,
        summarize_text,
    ]

# ── 3. Memory ─────────────────────────────────────────────────
def get_memory():
    return ConversationBufferMemory(
        memory_key="chat_history",   # must match the prompt variable
        return_messages=True         # returns as message objects, not raw string
    )

# ── 4. Build Agent ────────────────────────────────────────────
def build_agent():
    llm = get_llm()
    tools = get_tools()
    memory = get_memory()

    # conversational-react-description supports memory
    # this is different from Day 1's react prompt
    prompt = hub.pull("hwchase17/react-chat")

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )

    return agent_executor