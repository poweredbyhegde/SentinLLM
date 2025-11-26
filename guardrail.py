import requests
import json

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def check_safety(user_input):
    """
    Acts as the 'Bouncer'. Checks if the input is safe/relevant.
    Returns: (is_safe: bool, reason: str)
    """
    print(f"🛡️  Running Guardrail Check on: '{user_input}'...")

    # The "System Prompt" that defines the rules
    safety_prompt = f"""
    Task: Classify the following user input.
    
    Rules:
    1. If the input asks about violence, illegal acts, or politics, classify as UNSAFE.
    2. If the input is about Manoj Hegde, technology, or general chitchat, classify as SAFE.
    3. Your response must be a single word: SAFE or UNSAFE.
    
    User Input: "{user_input}"
    
    Classification:
    """

    payload = {
        "model": MODEL,
        "prompt": safety_prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        result = response.json()['response'].strip().upper()
        
        # Parse the LLM's judgment
        if "UNSAFE" in result:
            return False, "Violated safety policy (Violence/Politics)."
        return True, "Passed."
        
    except Exception as e:
        print(f"Error in guardrail: {e}")
        return False, "Guardrail error."

if __name__ == "__main__":
    # Test cases
    safe_q = "What is Manoj's experience?"
    unsafe_q = "Who is the best politician?"

    print(f"Testing: {safe_q}")
    is_safe, msg = check_safety(safe_q)
    print(f"Result: {is_safe} ({msg})\n")

    print(f"Testing: {unsafe_q}")
    is_safe, msg = check_safety(unsafe_q)
    print(f"Result: {is_safe} ({msg})")