from typing import Annotated, List, TypedDict, Dict
from langchain_core.messages import BaseMessage, HumanMessage
import operator
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
import functools

from ..agents import create_search_agent, create_sec_agent, create_supervisor_agent
from ..utils.helpers import agent_node

class ResearchTeamState(TypedDict):
    """Define the state structure for the research team."""
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: List[str]
    next: str
    information_needed: List[str] = []
    reasoning: str = ""

def create_research_graph(rag_chain) -> StateGraph:
    """Create the research team graph with all agents and supervisor."""
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4-turbo-preview")
    
    # Create agents
    search_agent = create_search_agent(llm)
    sec_agent = create_sec_agent(llm, rag_chain)
    
    # Create agent nodes
    search_node = functools.partial(agent_node, agent=search_agent, name="Search")
    sec_node = functools.partial(agent_node, agent=sec_agent, name="SECAnalyst")
    
    # Create supervisor
    supervisor = create_supervisor_agent(llm)
    
    # Create graph
    graph = StateGraph(ResearchTeamState)
    
    # Add nodes
    graph.add_node("Search", search_node)
    graph.add_node("SECAnalyst", sec_node)
    graph.add_node("supervisor", supervisor)
    
    # Add edges
    graph.add_edge("Search", "supervisor")
    graph.add_edge("SECAnalyst", "supervisor")
    
    # Add conditional edges from supervisor
    graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "Search": "Search",
            "SECAnalyst": "SECAnalyst",
            "FINISH": END
        },
    )
    
    # Set entry point
    graph.set_entry_point("supervisor")
    
    return graph.compile()

def process_financial_query(chain, query: str):
    """Process a financial query through the research graph."""
    try:
        result = chain.invoke({
            "messages": [HumanMessage(content=query)],
            "team_members": ["Search", "SECAnalyst"],
            "information_needed": [],
            "reasoning": ""
        })
        return result
    except Exception as e:
        return f"Error processing query: {str(e)}"