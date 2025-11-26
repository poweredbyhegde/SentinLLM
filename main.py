from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

# --- CONFIGURATION ---
# We force the endpoint to ensure it hits the local Phoenix server
tracer_provider = register(
    project_name="sentinllm",
    endpoint="http://127.0.0.1:6006/v1/traces"
)
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
# ---------------------

app = FastAPI(title="SentinLLM API", version="0.2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL = "llama3.2" # or "llama3"

class QueryRequest(BaseModel):
    prompt: str

class QueryResponse(BaseModel):
    response: str
    model: str

@app.get("/")
def health_check():
    return {"status": "active", "service": "SentinLLM"}

@app.post("/query", response_model=QueryResponse)
def query_llm(request: QueryRequest):
    try:
        print(f"📡 Sending prompt to {MODEL}...")
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": request.prompt}],
            temperature=0.0,
        )
        answer = completion.choices[0].message.content
        return QueryResponse(response=answer, model=MODEL)
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))