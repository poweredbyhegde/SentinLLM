import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
DATA_PATH = "data"
DB_PATH = "vector_db"  # Where we save the "brain"

def build_database():
    print("📚 Loading documents...")
    documents = []
    
    # Load all PDFs in the data directory
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(DATA_PATH, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
            print(f"   - Loaded: {file}")

    if not documents:
        print("❌ No PDF documents found in 'data/' folder!")
        return

    # Split text into chunks (so the AI can digest it)
    print("✂️  Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"   - Created {len(chunks)} text chunks.")

    # Create Embeddings (Turn text into numbers)
    # We use a free, local model from HuggingFace (no API key needed)
    print("🧠 Creating Vector Database (this may take a moment)...")
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Save to ChromaDB
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_function, 
        persist_directory=DB_PATH
    )
    
    print(f"✅ Success! Knowledge base saved to '{DB_PATH}'")

if __name__ == "__main__":
    build_database()