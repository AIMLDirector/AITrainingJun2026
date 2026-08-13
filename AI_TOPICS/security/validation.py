from fastapi import FastAPI
from pydantic import BaseModel
from detoxify import Detoxify

# Load model once (important for performance)
model = Detoxify("original")

app = FastAPI(title="Real-Time Content Safety API")

THRESHOLDS = {
    "toxicity": 0.5,
    "severe_toxicity": 0.5,
    "obscene": 0.5,
    "threat": 0.5,
    "insult": 0.5,
    "identity_attack": 0.5
}

class UserInput(BaseModel):
    text: str

@app.post("/validate")
def validate_text(input: UserInput):
    scores = model.predict(input.text)

    unsafe_reasons = []
    for category, score in scores.items():
        if score >= THRESHOLDS[category]:
            unsafe_reasons.append(f"{category} ({float(score):.2f})")

    is_safe = len(unsafe_reasons) == 0

    return {
        "input": input.text,
        "is_safe": is_safe,
        "scores": {k: float(v) for k, v in scores.items()},
        "reasons": unsafe_reasons
    }
