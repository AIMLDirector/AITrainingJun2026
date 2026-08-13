from openai import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from dotenv import load_dotenv
from huggingface_hub import login

load_dotenv()
login(token=os.getenv("HF_TOKEN"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load LlamaGuard LLM
model_name = "meta-llama/LlamaGuard-7b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype=torch.float16, device_map="auto"
)

SYSTEM_PROMPT = "Classify the following user text as safe or unsafe:\n\n"

def check_with_llama_guard(text: str) -> bool:
    prompt = SYSTEM_PROMPT + text + "\nAnswer:"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    output = model.generate(
        **inputs,
        max_new_tokens=10,
        do_sample=False
    )
    result = tokenizer.decode(output[0], skip_special_tokens=True).lower()
    print("LlamaGuard Response:", result)

    return "safe" in result.split()[:3]  # check first tokens

def safe_chat(user_input: str):
    if not check_with_llama_guard(user_input):
        return "⚠️ Your input was flagged as unsafe by LlamaGuard."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
        max_tokens=200,
    )
    return response.choices[0].message.content

print(safe_chat("Hello, how are you?"))
print(safe_chat("I hate all people of X group"))

