import requests
import json
import sys

# Import the RAG function from your existing script
# (Make sure secure_rag.py is in the same folder)
try:
    from secure_rag import run_rag_pipeline
except ImportError:
    print("❌ Error: Could not import 'secure_rag.py'. Make sure it exists!")
    sys.exit(1)

# --- CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/api/generate"
JUDGE_MODEL = "llama3.2" 

# --- THE GOLDEN DATASET ---
TEST_CASES = [
    {
        "question": "What is Manoj's current role?",
        "expected_fact": "Development Team Lead and Master's Student"
    },
    {
        "question": "Which university is he attending?",
        "expected_fact": "Paderborn University"
    },
    {
        "question": "What tech stack did he use at Webknot?",
        "expected_fact": "React, Next.js, Node.js, Spring Boot, MERN stack"
    },
    {
        "question": "Does he have any publications?",
        "expected_fact": "Yes, Springer publications on Chronic Kidney Disease and Voice Assistants"
    }
]

def evaluate_answer(question, actual_answer, expected_fact):
    """
    The 'LLM-as-a-Judge' Logic.
    """
    
    judge_prompt = f"""
    You are an impartial grader. Evaluate the AI's answer to the question based on the expected fact.
    
    Question: "{question}"
    Expected Fact: "{expected_fact}"
    AI Actual Answer: "{actual_answer}"
    
    Task:
    1. Does the AI's answer contain the specific information in the Expected Fact?
    2. Assign a score: 1 for Correct/Pass, 0 for Incorrect/Fail.
    3. Provide a very short reason.
    
    Format your response as valid JSON only:
    {{
        "score": 0 or 1,
        "reason": "short explanation"
    }}
    """

    payload = {
        "model": JUDGE_MODEL,
        "prompt": judge_prompt,
        "stream": False,
        "format": "json" # Enforces JSON output structure
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()['response']
        return json.loads(result)
    except Exception as e:
        return {"score": 0, "reason": f"Evaluation Error: {str(e)}"}

def run_evals():
    print("\n🧪 Starting SentinLLM Evaluation Pipeline...")
    print("=============================================")
    
    total_score = 0

    for i, test in enumerate(TEST_CASES):
        q = test["question"]
        expected = test["expected_fact"]
        
        print(f"\nTest #{i+1}: {q}")
        
        # 1. Run RAG Pipeline (The "Subject")
        print("   🤖 Generating RAG answer...")
        try:
            # This calls your existing RAG function
            actual_answer = run_rag_pipeline(q)
        except Exception as e:
            actual_answer = f"Pipeline Error: {str(e)}"
            
        # 2. Run Evaluator (The "Judge")
        print("   ⚖️  Judging answer...")
        eval_result = evaluate_answer(q, actual_answer, expected)
        
        # 3. Tally Score
        score = eval_result.get("score", 0)
        reason = eval_result.get("reason", "No reason provided")
        
        total_score += score
        
        # Visual Feedback
        status_icon = "✅ PASS" if score == 1 else "❌ FAIL"
        print(f"   {status_icon} (Score: {score}) | Reason: {reason}")

    # --- FINAL REPORT ---
    accuracy = (total_score / len(TEST_CASES)) * 100
    print("\n=============================================")
    print(f"📊 Evaluation Complete.")
    print(f"Total Score: {total_score}/{len(TEST_CASES)}")
    print(f"System Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 75:
        print("🚀 RESULT: PASSED - Pipeline is ready for deployment.")
    else:
        print("⚠️ RESULT: FAILED - RAG pipeline needs improvement.")

if __name__ == "__main__":
    run_evals()