import os
import streamlit as st
from openai import OpenAI
import anthropic
import google.generativeai as genai
from pypdf import PdfReader
from dotenv import load_dotenv

# ---------------- CONFIGURATION ----------------
load_dotenv()

# Load all potential keys
PROVIDERS = {
    "OpenRouter": os.getenv("OPENROUTER_API_KEY"),
    "Gemini": os.getenv("GOOGLE_API_KEY"),
    "OpenAI": os.getenv("OPENAI_API_KEY"),
    "Claude": os.getenv("ANTHROPIC_API_KEY")
}

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Multi-Provider PDF RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #e0e0e0;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- SIDEBAR: SETTINGS ----------------
with st.sidebar:
    st.title("⚙️ Settings")
    st.divider()
    
    # Provider selection
    provider = st.selectbox(
        "Select AI Provider",
        options=["OpenRouter", "Gemini", "OpenAI", "Claude"],
        index=0
    )
    
    # Model selection based on provider
    if provider == "OpenRouter":
        model_name = st.selectbox(
            "Select Free Model",
            options=["qwen/qwen3.6-plus:free", "nvidia/nemotron-3-super:free"],
            help="High-quality free models via OpenRouter."
        )
    elif provider == "Gemini":
        model_name = st.selectbox(
            "Select Gemini Model",
            options=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
            index=2
        )
    elif provider == "OpenAI":
        model_name = st.selectbox(
            "Select OpenAI Model",
            options=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
            index=1
        )
    elif provider == "Claude":
        model_name = st.selectbox(
            "Select Claude Model",
            options=["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
            index=0
        )

    # Key validation
    if not PROVIDERS[provider]:
        st.error(f"⚠️ {provider} API Key missing in .env")
    else:
        st.success(f"✅ {provider} Key found.")
        
    st.divider()
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ---------------- CORE CHAT FUNCTIONS ----------------
def get_llm_response(provider, model, prompt, context):
    """Router to call the correct LLM provider"""
    system_prompt = "You are a helpful assistant. Use the provided context to answer the user's question accurately. If the answer is not in the context, refer to it as 'not explicitly mentioned in the document'."
    full_prompt = f"Context:\n{context}\n\nUser Question: {prompt}"

    try:
        if provider == "OpenRouter" or provider == "OpenAI":
            # Both use the OpenAI-compatible SDK
            base_url = "https://openrouter.ai/api/v1" if provider == "OpenRouter" else None
            client = OpenAI(api_key=PROVIDERS[provider], base_url=base_url)
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ]
            )
            return response.choices[0].message.content

        elif provider == "Gemini":
            genai.configure(api_key=PROVIDERS[provider])
            gemini_model = genai.GenerativeModel(model)
            response = gemini_model.generate_content(f"{system_prompt}\n{full_prompt}")
            return response.text

        elif provider == "Claude":
            client = anthropic.Anthropic(api_key=PROVIDERS[provider])
            message = client.messages.create(
                model=model,
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": full_prompt}]
            )
            return message.content[0].text

    except Exception as e:
        return f"Error from {provider}: {str(e)}"

# ---------------- PDF UTILITIES ----------------
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            res = page.extract_text()
            if res: text += res + "\n"
        return text
    except Exception as e:
        st.error(f"PDF Error: {e}")
        return None

def retrieve_context(question, document, top_k=8):
    if not document: return ""
    lines = [l.strip() for l in document.split("\n") if l.strip()]
    scored = []
    q_words = set(question.lower().split())
    for line in lines:
        score = sum(1 for w in q_words if w in line.lower())
        if score > 0: scored.append((score, line))
    scored.sort(key=lambda x: x[0], reverse=True)
    return "\n".join([l for s, l in scored[:top_k]])

# ---------------- MAIN UI ----------------
st.title("🤖 Multi-Provider PDF RAG Chatbot")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# File Upload
uploaded_file = st.file_uploader("📂 Upload your PDF", type=["pdf"])

if uploaded_file:
    # Caching document content
    if "doc_text" not in st.session_state or st.session_state.get("last_uploaded") != uploaded_file.name:
        with st.spinner("Analyzing document..."):
            st.session_state.doc_text = extract_text_from_pdf(uploaded_file)
            st.session_state.last_uploaded = uploaded_file.name
    
    doc_text = st.session_state.doc_text
    
    if doc_text:
        st.success(f"✅ Loaded: {uploaded_file.name}")
        
        # Chat display
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        # Chat Input
        if prompt := st.chat_input("Ask a question about this PDF..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Process response
            with st.spinner(f"Getting answer from {provider} ({model_name})..."):
                context = retrieve_context(prompt, doc_text)
                answer = get_llm_response(provider, model_name, prompt, context)
                
                with st.chat_message("assistant"):
                    st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
    else:
        st.error("Failed to extract content.")
else:
    st.info("👋 Welcome! Select a provider in the sidebar and upload a PDF to start.")

# Footer
st.markdown("---")
st.caption("AI RAG Orchestrator | Supports OpenAI, Claude, Gemini & OpenRouter")
