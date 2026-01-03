from openai import OpenAI

client = OpenAI()

question = input("Ask something: ")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": question}
    ]
)

print("\nAI Answer:")
print(response.choices[0].message.content)
