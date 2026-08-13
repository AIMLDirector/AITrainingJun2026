from openai import OpenAI
from transformers import pipeline
import os
from dotenv import load_dotenv
from huggingface_hub import login
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ✅ Load environment variables
load_dotenv()

# Hugging Face auth (optional if model is public)
huggingface_token = os.environ.get("HF_TOKEN")
if huggingface_token:
    login(token=huggingface_token)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

moderator = pipeline(
    "text-classification",
    model="facebook/roberta-hate-speech-dynabench-r4-target",
    top_k=None  # replaces return_all_scores=True
)

def check_with_moderator(text: str) -> bool:
    """
    Runs text through HF moderation model.
    Returns True if considered safe, False otherwise.
    """
    results = moderator(text)
    scores = results[0]  # list of dicts
    best = max(scores, key=lambda x: x["score"])
    print(f"Moderation result: {best}")
    return best["label"].lower() == "nothate"

def safe_chat(user_input: str) -> str:
    """
    Routes safe messages to OpenAI, blocks unsafe.
    """
    if check_with_moderator(user_input):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    else:
        return "⚠️ Your input was flagged as unsafe by the moderation model."


print(safe_chat("Hello, how are you?"))           
print(safe_chat("I hate all people of X group"))

