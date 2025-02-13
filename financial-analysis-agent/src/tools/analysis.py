from typing import Annotated
from langchain_core.tools import tool

@tool
def retrieve_information(
    query: Annotated[str, "query to analyze financial documents"],
    rag_chain=None
):
    """Use RAG to get specific information from financial documents."""
    if rag_chain is None:
        return "RAG chain not initialized"
    return rag_chain.invoke(query)

@tool
def analyze_financials(
    query: Annotated[str, "query to analyze financial metrics"]
):
    """Analyze financial metrics and ratios."""
    # Add financial analysis logic here
    pass