# 🛡️ SentinLLM: Automated Guardrails & Eval Pipeline

**SentinLLM** is a production-grade **LLM Ops (Large Language Model Operations)** system designed to make Generative AI safe, reliable, and measurable.

Instead of just deploying a chatbot, this project builds the **infrastructure** around the LLM. It implements a **"Smart Proxy"** layer that intercepts user queries, enforces safety guardrails, retrieves private context (RAG), and automatically evaluates the quality of responses using an "LLM-as-a-Judge" framework.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=yellow)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?logo=ollama)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-orange)

---
## 📺 Demo

https://github.com/user-attachments/assets/a40d5f45-047f-4df9-8440-9b434fa4bd16

---



## 🏗️ System Architecture

The pipeline transforms a raw LLM into a secure, business-ready application:

1.  **The Brain (Model):** A local **Llama 3** model running in a Dockerized **Ollama** server.
2.  **The Bouncer (Guardrails):** A custom pre-processing layer that intercepts user prompts. It uses an LLM classifier to detect and block unsafe content (e.g., politics, violence) *before* it reaches the core logic.
3.  **The Memory (RAG):** A **Retrieval Augmented Generation** pipeline using **ChromaDB** and **HuggingFace Embeddings**. It allows the AI to answer questions based on private documents (e.g., a resume) without hallucinations.
4.  **The Auditor (Evaluations):** An automated testing suite (`run_evals.py`) that uses a "Judge Model" to score the system's answers against a Golden Dataset, calculating a strict accuracy percentage.

---

## 🚀 Key Features

* **🔒 Active Guardrails:** Blocks malicious or off-topic inputs instantly, ensuring the bot stays compliant with safety guidelines.
* **📚 Private RAG:** Ingests PDF documents (like resumes or manuals), chunks them, and retrieves relevant context to ground the AI's answers in fact.
* **⚖️ Automated Evals:** Features an "LLM-as-a-Judge" pipeline that runs test cases and grades the AI's output (Pass/Fail) to detect regressions or hallucinations automatically.
* **🐳 Fully Local & Private:** Runs 100% offline using Docker and Ollama—no data is sent to OpenAI or external APIs.


---

## 🛠️ How to Run Locally

### Prerequisites
* Docker & Docker Compose
* Python 3.11+ (in a virtual environment)

### 1. Start the Infrastructure
Spin up the local Ollama instance using Docker.
docker-compose up -d

### 2. Pull the Model
Once the container is running, pull the Llama 3 model (this happens inside the container):
docker exec -it sentinllm_ollama ollama run llama3.2

### 3. Add Your Data (RAG Knowledge Base)
This project uses your own data to answer questions.
Create a folder named data/ in the root directory.
Add your PDF files (e.g., resume.pdf, manual.pdf) into the data/ folder.
Run the ingestion script to build the Vector Database:

python build_knowledge.py

### 4. Run the Dashboard (UI)
Start the Streamlit application to interact with the secure chat agent.
streamlit run app.py

Try asking questions based on the PDFs you uploaded. The Guardrail will block unsafe questions (like "how to hack"), while RAG will answer relevant questions.

### 5. Run Automated Evaluations
Execute the test suite to grade the AI's performance against the Golden Dataset (edit run_evals.py to match your specific data).
python run_evals.py


---
## 👨‍💻 Connect with Me

This project was built with a lot of coffee and (many) failed CI/CD runs. Find me here:
[![Portfolio](https://img.shields.io/badge/Portfolio-manoj--hegde.com-7025F5?style=flat&logo=dribbble&logoColor=white)](https://manoj-hegde.com)
