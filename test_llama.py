import ollama

response = ollama.chat(
    model='llama3',
    messages=[
        {"role": "user", "content": "Hello, who are you?"}
    ]
)

print(response['message']['content'])