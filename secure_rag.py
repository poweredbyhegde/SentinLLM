import requests
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# --- CONFIGURATION ---
DB_PATH = "vector_db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

# --- COMPONENT 1: THE GUARDRAIL (The Bouncer) ---
def check_safety(user_input):
    print(f"🛡️  Checking Safety for: '{user_input}'...")
    
    safety_prompt = f"""
    Task: Classify the following user input.
    
    Rules:
    1. If the input asks about violence, illegal acts, politics, or anything NSFW, classify as UNSAFE.
    2. If the input is about Manoj Hegde, technology, coding, or general professional greetings, classify as SAFE.
    3. Your response must be a single word: SAFE or UNSAFE.
    
    User Input: "{user_input}"
    
    Classification:
    """
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": safety_prompt,
            "stream": False
        })
        result = response.json()['response'].strip().upper()
        
        if "UNSAFE" in result:
            return False, "I cannot answer that question due to safety guidelines."
        return True, "Safe."
    except Exception as e:
        return True, "Guardrail error (failing open for demo)." # Fail safe/open logic

# --- COMPONENT 2: THE RAG ENGINE (The Brain) ---
def run_rag_pipeline(question):
    # 1. Initialize DB
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)

    # 2. Retrieve Context
    print("🔍 Searching Resume Database...")
    results = db.similarity_search(question, k=3)
    
    if not results:
        return "I couldn't find any information about that in Manoj's resume."

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])

    # 3. Generate Answer
    prompt = f"""
    You are a helpful assistant for Manoj Hegde.
    Use ONLY the context below to answer the question.
    If the answer is not in the context, say you don't know.
    
    Context:
    {context_text}
    
    Question:
    {question}
    """
    
    print("🤖 Generating Answer...")
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']

# --- MAIN PIPELINE ---
if __name__ == "__main__":
    print("\n🔒 SentinLLM Secure System Online.")
    print("-----------------------------------")
    
    while True:
        try:
            user_input = input("\n❓ Ask about Manoj: ")
            if user_input.lower() in ['exit', 'quit']: break
            if not user_input.strip(): continue

            # STEP 1: GUARDRAIL
            is_safe, message = check_safety(user_input)
            
            if not is_safe:
                print(f"\n🚫 BLOCKED: {message}")
                continue # Skip the rest, ask for new input

            # STEP 2: RAG
            answer = run_rag_pipeline(user_input)
            print(f"\n💡 Answer: {answer}")
            print("-" * 30)

        except KeyboardInterrupt:
            print("\n👋 Exiting.")
            break