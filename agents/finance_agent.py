from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain import hub
from tools.crypto import get_crypto_price
from dotenv import load_dotenv
import os

load_dotenv()

def build_finance_agent() -> AgentExecutor:
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    def calculator(expression: str) -> str:
        """
        ALWAYS use for ANY math calculation.
        Input must be a Python math expression like '8333 * 12'.
        """
        try:
            return str(eval(expression))
        except Exception as e:
            return f"Error: {str(e)}"
        
    tools = [
        get_crypto_price,
        Tool(
            name="calculator",
            func=calculator,
            description="""ALWAYS use this tool for ANY mathematical
            calculation. Never do math in your head.
            Input must be a valid Python expression like '8333 * 12'."""
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