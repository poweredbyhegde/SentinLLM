import requests
import json

# Configuration
# Ollama API endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def query_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False  # Get one complete response object
    }
    
    print(f"🤖 Sending query: '{prompt}'...")
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['response']
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the connection
    question = "Explain what 'Guardrails' are in AI in one simple sentence."
    answer = query_llm(question)
    
    print("\n💡 LLM Answer:")
    print(answer)