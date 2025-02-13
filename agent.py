from typing import Any, Callable, List, Optional, TypedDict, Union, Annotated
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langchain_community.tools.tavily_search import TavilySearchResults
import functools
import operator

# Initialize Tavily
tavily_tool = TavilySearchResults(max_results=5)