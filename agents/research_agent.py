from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from dotenv import load_dotenv
import os

load_dotenv()

def build_research_agent() -> AgentExecutor:
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    search = TavilySearchResults(
        api_key=os.getenv("TAVILY_API_KEY"),
        max_results=3
    )

    tools = [
        Tool(
            name="web_search",
            func=search.run,
            description="""ALWAYS use this to search for news, facts, 
            people, companies, events, or any current information."""
        )
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
        max_iterations=4,
        handle_parsing_errors=True
    )