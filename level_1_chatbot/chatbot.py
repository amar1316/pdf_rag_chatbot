from openai import OpenAI

client = OpenAI()

# 🧠 Memory (message history)
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]

print("🤖 Chatbot started (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    # Add user message to memory
    messages.append({"role": "user", "content": user_input})

    # Call LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    ai_reply = response.choices[0].message.content

    # Add AI response to memory
    messages.append({"role": "assistant", "content": ai_reply})

    print("AI:", ai_reply)
