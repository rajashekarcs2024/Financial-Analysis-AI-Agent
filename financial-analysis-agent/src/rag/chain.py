from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from .loader import DocumentLoader

def create_rag_chain(file_path: str = "data/raw/apple_10k.pdf"):
    # Load and split document
    loader = DocumentLoader(file_path)
    split_chunks = loader.load_and_split()
    
    # Create embeddings and vectorstore
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Qdrant.from_documents(
        split_chunks,
        embedding_model,
        location=":memory:",
        collection_name="apple_10k",
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever()
    
    # Create prompt
    template = """You are a financial analyst. Use the provided context to answer questions about the company's financials.
    
    Context: {context}
    Question: {question}
    
    Answer the question based on the context provided. Include specific numbers and data when available."""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | ChatOpenAI(model="gpt-4-turbo-preview")
        | StrOutputParser()
    )
    
    return chain