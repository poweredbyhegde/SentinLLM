import requests
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
DB_PATH = "vector_db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def query_rag(question):
    # 1. Initialize Embedding Function
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 2. Connect to the Database
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)

    # 3. Retrieve relevant context
    print(f"\n🔍 Searching knowledge base for: '{question}'...")
    results = db.similarity_search(question, k=3)
    
    if not results:
        print("   ⚠️ No relevant context found.")
        return "I couldn't find any information about that in the documents."

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    print(f"   - Found {len(results)} relevant context chunks.")

    # 4. Construct the Prompt
    prompt = f"""
    You are an intelligent assistant representing Manoj Hegde. 
    Answer the question based ONLY on the following context provided from his resume.
    If the answer is not in the context, say "I don't know based on the available information."
    
    Context:
    {context_text}
    
    Question:
    {question}
    """

    # 5. Send to Ollama
    print("🤖 Asking Llama 3...")
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['response']
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("💬 SentinLLM RAG System Ready! Type 'exit' to quit.")
    print("--------------------------------------------------")
    
    while True:
        try:
            user_query = input("\n❓ Ask a question about Manoj: ")
            if user_query.lower() in ['exit', 'quit']:
                print("👋 Exiting.")
                break
            if not user_query.strip():
                continue
                
            answer = query_rag(user_query)
            print("\n💡 Answer:")
            print(answer)
            print("-" * 30)
        except KeyboardInterrupt:
            print("\n👋 Exiting.")
            break
EOFcat <<EOF > query_rag.py
import requests
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration
DB_PATH = "vector_db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def query_rag(question):
    # 1. Initialize Embedding Function
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 2. Connect to the Database
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)

    # 3. Retrieve relevant context
    print(f"\n🔍 Searching knowledge base for: '{question}'...")
    results = db.similarity_search(question, k=3)
    
    if not results:
        print("   ⚠️ No relevant context found.")
        return "I couldn't find any information about that in the documents."

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    print(f"   - Found {len(results)} relevant context chunks.")

    # 4. Construct the Prompt
    prompt = f"""
    You are an intelligent assistant representing Manoj Hegde. 
    Answer the question based ONLY on the following context provided from his resume.
    If the answer is not in the context, say "I don't know based on the available information."
    
    Context:
    {context_text}
    
    Question:
    {question}
    """

    # 5. Send to Ollama
    print("🤖 Asking Llama 3...")
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['response']
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("💬 SentinLLM RAG System Ready! Type 'exit' to quit.")
    print("--------------------------------------------------")
    
    while True:
        try:
            user_query = input("\n❓ Ask a question about Manoj: ")
            if user_query.lower() in ['exit', 'quit']:
                print("👋 Exiting.")
                break
            if not user_query.strip():
                continue
                
            answer = query_rag(user_query)
            print("\n💡 Answer:")
            print(answer)
            print("-" * 30)
        except KeyboardInterrupt:
            print("\n👋 Exiting.")
            break
