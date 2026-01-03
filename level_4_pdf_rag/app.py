import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

client = OpenAI()

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="PDF RAG Chatbot", layout="centered")
st.title("📄 PDF RAG Chatbot")
st.write("Upload a PDF and ask questions based only on its content")

# ---------------- PDF UPLOAD ----------------
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# ---------------- SIMPLE RETRIEVER ----------------
def retrieve_context(question, document):
    lines = document.split("\n")
    relevant = []

    for line in lines:
        for word in question.split():
            if word.lower() in line.lower():
                relevant.append(line)
                break

    return "\n".join(relevant[:5])

# ---------------- SESSION MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer ONLY from the given context. If not found, say you don't know."
        }
    ]

# ---------------- CHAT UI ----------------
if uploaded_file:
    document_text = extract_text_from_pdf(uploaded_file)
    st.success("PDF loaded successfully")

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask a question from the PDF...")

    if user_input:
        context = retrieve_context(user_input, document_text)

        if context.strip() == "":
            context = "No relevant information found in the document."

        user_prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{user_input}
"""

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages + [
                {"role": "user", "content": user_prompt}
            ]
        )

        reply = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

else:
    st.info("Please upload a PDF to start chatting.")
