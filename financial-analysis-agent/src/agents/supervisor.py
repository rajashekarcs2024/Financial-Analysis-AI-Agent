from langchain_openai import ChatOpenAI
from ..utils.helpers import create_team_supervisor

def create_supervisor_agent(llm: ChatOpenAI):
    """Creates the supervisor agent for financial research."""
    
    supervisor_prompt = """You are a supervisor tasked with managing a conversation between
    Search and SECAnalyst workers. 
    
    Think step by step:
    1. What specific financial information is needed to fully answer the query?
    2. Which agent is best suited to find each piece of information?
    3. What order of operations would give the most comprehensive answer?
    4. Have we gathered all necessary information to FINISH?

    Search worker: Use for market data, competitor analysis, analyst views
    SECAnalyst worker: Use for historical data, financial metrics, regulatory insights
    
    When agents request additional context:
    1. Route to appropriate agent for that information
    2. Ensure the response addresses the original query
    3. Only FINISH when you have:
       - Gathered all necessary information from both sources if needed
       - Confirmed the response addresses the original query comprehensively
       - Validated that no additional context is needed
    
    Coordinate between agents until you have a complete analysis."""
    
    return create_team_supervisor(
        llm=llm,
        system_prompt=supervisor_prompt,
        members=["Search", "SECAnalyst"]
    )