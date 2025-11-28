import requests
import json
import sys

# Import RAG components
# If these fail, ensure you ran: pip install langchain-huggingface langchain-chroma
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma
except ImportError as e:
    print(f"❌ Library Error: {e}")
    print("Please run: pip install langchain-huggingface langchain-chroma sentence-transformers")
    sys.exit(1)

# --- CONFIGURATION ---
DB_PATH = "vector_db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

# --- COMPONENT 1: THE GUARDRAIL (The Bouncer) ---
def check_safety(user_input):
    print(f"🛡️  Checking Safety for: '{user_input}'...")
    
    # Updated prompt to prevent "Prompt Injection" bypass
    safety_prompt = f"""
    Task: Classify the following user input as SAFE or UNSAFE.
    
    CRITICAL RULES:
    1. If the input asks for illegal acts, violence, hacking, malicious activities, or politics, it is UNSAFE.
    2. Safety rules OVERRIDE all other rules. Even if the input mentions "Manoj" or "Technology", if it asks for hacking or violence, it is UNSAFE.
    3. Only if the input is safe AND (about Manoj Hegde OR technology OR professional greeting), classify as SAFE.
    
    User Input: "{user_input}"
    
    Classification (Respond with only one word: SAFE or UNSAFE):
    """
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": safety_prompt,
            "stream": False
        })
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        result = data.get('response', '').strip().upper()
        
        if "UNSAFE" in result:
            return False, "I cannot answer that question due to safety guidelines."
            
        return True, "Safe."
        
    except Exception as e:
        print(f"⚠️ Guardrail Error: {e}")
        # Fail OPEN for demo purposes (allow if guardrail crashes), 
        # but in production you might want to Fail CLOSED (block).
        return True, "Guardrail bypassed due to error." 

# --- COMPONENT 2: THE RAG ENGINE (The Brain) ---
def run_rag_pipeline(question):
    try:
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
        response.raise_for_status()
        
        data = response.json()
        
        if "response" not in data:
            return f"Error: Ollama returned invalid JSON: {data}"
            
        return data['response']
        
    except Exception as e:
        return f"System Error: {str(e)}"

# --- MAIN PIPELINE ---
if __name__ == "__main__":
    print("\n🔒 SentinLLM Secure System Online.")
    print("-----------------------------------")
    
    while True:
        try:
            user_input = input("\n❓ Ask about Manoj: ")
            
            # Exit conditions
            if user_input.lower() in ['exit', 'quit']: 
                print("👋 Exiting.")
                break
            if not user_input.strip(): 
                continue

            # STEP 1: GUARDRAIL
            is_safe, message = check_safety(user_input)
            
            if not is_safe:
                print(f"\n🚫 BLOCKED: {message}")
                continue # Skip the rest, ask for new inpu
            # STEP 2: RAG
            answer = run_rag_pipeline(user_input)
            print(f"\n💡 Answer: {answer}")
            print("-" * 30)

        except KeyboardInterrupt:
            print("\n👋 Exiting.")
            break