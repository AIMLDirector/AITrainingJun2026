from transformers import pipeline
from huggingface_hub import login
from openai import OpenAI
from dotenv import load_dotenv
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()

login(token=os.getenv("HF_TOKEN"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Use LlamaGuard3 moderation
llamaguard = pipeline(
    "text-classification",
    model="meta-llama/Llama-Guard-3-8B",
    device_map="auto"
)

hate_speech = pipeline(
    "text-classification",
    model="Hate-speech-CNERG/english-abusive-MuRIL"
)

def check_moderation(text):
    reasons = []

    # LlamaGuard3 result
    lg = llamaguard(text)[0]
    if lg["label"].lower() != "safe":
        reasons.append("general unsafe (LlamaGuard3)")

    # Hate speech model
    hs = hate_speech(text)[0]
    if hs["label"] == "LABEL_1":
        reasons.append("hate speech")

    is_safe = len(reasons) == 0
    print(f"Moderation check - is_safe: {is_safe}, reasons: {reasons}")
    return is_safe, reasons


def safe_chat(user_input):
    is_safe, reasons = check_moderation(user_input)

    if not is_safe:
        return f"⚠️ Input flagged: {', '.join(reasons)}"

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful and polite assistant."},
            {"role": "user", "content": user_input},
        ],
        max_tokens=300,
    )
    return res.choices[0].message.content


print(safe_chat("Tell me a joke about religion"))
print(safe_chat("Hello!"))
print(safe_chat("I hate all people of X group"))
