import streamlit as st
import time
from secure_rag import check_safety, run_rag_pipeline

# --- UI CONFIGURATION ---
st.set_page_config(page_title="SentinLLM Dashboard", page_icon="🛡️", layout="wide")

# Sidebar for System Status
with st.sidebar:
    st.header("🛡️ System Status")
    st.success("✅ Model: Llama 3.2 (Local)")
    st.success("✅ Vector DB: ChromaDB (Online)")
    st.info("🔒 Guardrails: Active")
    
    st.divider()
    st.markdown("### 📊 Metrics")
    st.metric(label="Safety Score", value="100%")
    st.metric(label="RAG Latency", value="1.2s")

# Main Chat Interface
st.title("🛡️ SentinLLM: Secure RAG Agent")
st.markdown("Ask questions about **Manoj Hegde** (Professional context only).")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    # Set custom avatars based on role
    if message["role"] == "user":
        avatar = "/Users/manoj/projects /sentinllm/data/porfolio-image.png"  # OR use an emoji like "🧑‍💻"
    else:
        avatar = "/Users/manoj/projects /sentinllm/data/agent.jpg"      # OR use an emoji like "🛡️"
        
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Example: What is Manoj's tech stack?"):
    # 1. Show User Message (Add avatar here)
    st.chat_message("user", avatar="/Users/manoj/projects /sentinllm/data/porfolio-image.png").markdown(prompt) # <--- UPDATE THIS
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Run Guardrails (The Bouncer)
    with st.status("🔒 Checking Safety Guardrails...", expanded=True) as status:
        is_safe, safety_msg = check_safety(prompt)
        
        if not is_safe:
            status.update(label="❌ Blocked by Guardrail!", state="error", expanded=True)
            error_msg = f"**Security Alert:** {safety_msg}"
            st.chat_message("assistant").markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.stop() # Stop execution here
            
        status.update(label="✅ Guardrail Passed", state="complete", expanded=False)

# 3. Run RAG Pipeline (The Brain)
    # Add avatar here
    with st.chat_message("assistant", avatar="/Users/manoj/projects /sentinllm/data/agent.jpg"): # <--- UPDATE THIS
        message_placeholder = st.empty()
        # ... rest of code ...
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 Retrieving context and thinking...")
        
        # Measure latency (optional simulation)
        start_time = time.time()
        
        # Call your existing backend
        try:
            response = run_rag_pipeline(prompt)
        except Exception as e:
            response = f"System Error: {str(e)}"
            
        message_placeholder.markdown(response)
        
        # Save to history
        st.session_state.messages.append({"role": "assistant", "content": response})