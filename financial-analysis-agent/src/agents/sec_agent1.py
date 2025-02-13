from ..utils.helpers import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool

def create_sec_agent(llm: ChatOpenAI, rag_chain):
    """Create an agent specialized in SEC filings analysis."""
    
    system_prompt = """You are a financial analyst specialized in SEC filings analysis.
    Focus on extracting key metrics, risk factors, and financial statements from 
    company documents. Provide precise insights with specific numbers and data."""
    
    # Create the retrieval tool with proper binding to rag_chain
    retrieve_tool = Tool(
        name="retrieve_information",
        func=lambda x: rag_chain.invoke(x),
        description="""Use this tool to analyze SEC filings and extract specific 
        information from financial documents. Input should be a clear question 
        about financial metrics, risks, or statements."""
    )
    
    return create_agent(
        llm=llm,
        tools=[retrieve_tool],
        system_prompt=system_prompt
    )