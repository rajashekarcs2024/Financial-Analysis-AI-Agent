from dotenv import load_dotenv
from src.rag.chain import create_rag_chain
from src.graph.state import create_research_graph

def init_financial_system():
    """Initialize the RAG and research chain"""
    rag_chain = create_rag_chain("data/raw/apple_10k.pdf")
    chain = create_research_graph(rag_chain)
    return chain

if __name__ == "__main__":
    load_dotenv()
    from src.agentverse.register import run_agent
    run_agent()