from dotenv import load_dotenv
from src.rag.chain import create_rag_chain

def test_rag():
    # Initialize RAG chain
    print("Creating RAG chain...")
    rag_chain = create_rag_chain("data/raw/apple_10k.pdf")
    
    # Test queries
    test_questions = [
        "What is Apple's total revenue?",
        "What are the main risk factors?",
        "How much was spent on R&D?"
    ]
    
    # Test each question
    for question in test_questions:
        print(f"\nQuestion: {question}")
        try:
            response = rag_chain.invoke(question)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    test_rag()