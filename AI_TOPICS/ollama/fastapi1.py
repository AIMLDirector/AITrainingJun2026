# app.py
from fastapi import FastAPI
from ollama import chat

app = FastAPI()

@app.post("/ask")
def ask_llm(question: str):
    response = chat(
        model="qwen3.5:2b",
        messages=[{"role": "user", "content": question}]
    )
    return {"answer": response["message"]["content"]}