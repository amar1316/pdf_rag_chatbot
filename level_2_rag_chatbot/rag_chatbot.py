from openai import OpenAI

client = OpenAI()

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

    return "\n".join(relevant[:3])  # top 3 lines only

# ---------------- CHATBOT MEMORY ----------------
messages = [
    {"role": "system", "content": "You are a helpful assistant. Answer ONLY from the provided context."}
]

print("🤖 RAG Chatbot started (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    # 🔹 RAG STEP
    context = retrieve_context(user_input, document)

    if context.strip() == "":
        context = "No relevant information found in the document."

    # Add user message with context
    messages.append({
        "role": "user",
        "content": f"""
Use the following context to answer.

Context:
{context}

Question:
{user_input}
"""
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    print("AI:", reply)
