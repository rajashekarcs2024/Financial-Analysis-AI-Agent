from typing import Annotated
from langchain_core.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def tavily_search(query: str) -> str:
    """Search for real-time information using Tavily."""
    result = tavily_client.search(query)
    return str(result)