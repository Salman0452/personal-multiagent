from langchain.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

@tool
def summarize_text(text: str) -> str:
    """
    Summarize any long text into 3-5 clear bullet points.
    Input should be the full text you want summarized.
    Use this when user asks to summarize, shorten, or extract key points.
    """

    try:
        llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192",
            temperature=0,
        )
        prompt = f"""Summarize the following text into 3-5 clear bullet points.
Be concise and capture only the most important information.

Text:
{text}

Summary:"""
        
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error summarizing text: {str(e)}"