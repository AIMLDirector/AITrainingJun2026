import os
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# -------------------------
# Environment Setup
# -------------------------
os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()

login(token=os.getenv("HF_TOKEN"))

# -------------------------
# Load Llama-Guard-3 Model
# -------------------------
MODEL_ID = "meta-llama/Llama-Guard-3-8B"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",          # mps / cpu / gpu
    torch_dtype=torch.float16
)

llamaguard = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(title="Llama-Guard-3 Moderation API")

class UserInput(BaseModel):
    text: str

# -------------------------
# Llama-Guard Prompt
# -------------------------
def run_llamaguard(text: str):
    prompt = f"""
[INST] You are Llama Guard, a safety classifier.

Classify the following user input:

{text}

Answer with only:
SAFE
or
UNSAFE
[/INST]
"""
    output = llamaguard(prompt, max_new_tokens=50)[0]["generated_text"]
    return output.lower()

# -------------------------
# Moderation Endpoint
# -------------------------
@app.post("/moderate")
def moderate(input: UserInput):
    result = run_llamaguard(input.text)

    is_safe = "unsafe" not in result

    return {
        "input": input.text,
        "decision": "SAFE" if is_safe else "UNSAFE",
        "raw_output": result
    }
