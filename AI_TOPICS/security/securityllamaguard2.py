from transformers import pipeline
from huggingface_hub import login
from openai import OpenAI
from dotenv import load_dotenv
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()
# Hugging Face & OpenAI setup
login(token=os.getenv("HF_TOKEN"))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load moderation models
llamaguard = pipeline("text-classification", model="meta-llama/LlamaGuard-7b", device_map="auto")
hate_speech = pipeline("text-classification", model="Hate-speech-CNERG/english-abusive-MuRIL", top_k=None)

def check_moderation(text: str):
    reasons = []

    # --- LlamaGuard ---
    llama_result = llamaguard(text)[0]
    llama_label = "safe" if llama_result["label"] == "LABEL_0" else "unsafe"
    if llama_label == "unsafe":
        reasons.append("general unsafe (LlamaGuard)")

    # --- Hate Speech ---
    hate_result = hate_speech(text)[0]  # returns a list of dicts
    # pick the label with the highest score
    top_label = max(hate_result, key=lambda x: x["score"])["label"]

    # In this model: LABEL_0 = nothate, LABEL_1 = hate
    hate_label = "hate" if top_label == "LABEL_1" else "nothate"
    if hate_label == "hate":
        reasons.append("hate speech")

    # Final decision
    is_safe = (len(reasons) == 0)
    print(f"Moderation check - is_safe: {is_safe}, reasons: {reasons}")
    return is_safe, reasons


# --- Safe Chat ---
def safe_chat(user_input: str):
    is_safe, reasons = check_moderation(user_input)

    if not is_safe:
        return f"⚠️ Your input was flagged as unsafe: {', '.join(reasons)}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful and polite assistant."},
            {"role": "user", "content": user_input},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content


# --- Test ---
print(safe_chat("Hello, how are you?"))             # ✅ should pass
print(safe_chat("I hate all people of X group"))    # ⚠️ should flag as hate
print(safe_chat("Tell me a joke about a sensitive topic."))  # may flag as unsafe