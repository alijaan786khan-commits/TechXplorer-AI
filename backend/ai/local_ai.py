from ollama import chat

def ask_ai(prompt):
    response = chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]