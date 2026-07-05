from fastapi import FastAPI
import uvicorn

from ai.local_ai import ask_ai

app = FastAPI(title="TechXplorer AI")

@app.get("/")
def home():
    return {
        "message": "Welcome to TechXplorer AI"
    }

@app.get("/chat")
def chat(prompt: str):
    answer = ask_ai(prompt)
    return {
        "question": prompt,
        "answer": answer
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)