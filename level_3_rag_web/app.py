import streamlit as st
from openai import OpenAI

client = OpenAI()

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("📄 RAG Chatbot")
st.write("Ask questions based only on the document")

# ---------------- LOAD DATA ----------------
with open("data.txt", "r") as f:
    document = f.read()

# ---------------- SIMPLE RETRIEVER ----------------
def retrieve_context(question, document):
    lines = document.split("\n")
    relevant = []

    for line in lines:
        for word in question.split():
            if word.lower() in line.lower():
                relevant.append(line)
                break

    return "\n".join(relevant[:3])

# ---------------- SESSION MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Answer only from the given context."}
    ]

# ---------------- CHAT UI ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask a question...")

if user_input:
    # RAG step
    context = retrieve_context(user_input, document)
    if context.strip() == "":
        context = "No relevant information found in the document."

    user_prompt = f"""
Use the following context to answer.

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
# ---------------- RESET BUTTON ----------------