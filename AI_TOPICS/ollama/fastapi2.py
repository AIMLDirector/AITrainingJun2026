from fastapi import FastAPI
from pydantic import BaseModel
from ollama import chat

app = FastAPI()

# Request Model
class QuestionRequest(BaseModel):
    question: str

# Response Model
class AnswerResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=AnswerResponse)
def ask_llm(request: QuestionRequest):
    response = chat(
        model="qwen3.5:2b",
        messages=[
            {"role": "user", "content": request.question}
        ]
    )

    return AnswerResponse(answer=response["message"]["content"])