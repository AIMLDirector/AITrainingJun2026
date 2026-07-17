import torch
from transformers import pipeline

# Load the instruction-tuned model and tokenizer
model_id = "meta-llama/Llama-3.2-1B-Instruct"

pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

messages = [
    {"role": "system", "content": "You are a concise, helpful assistant."},
    {"role": "user", "content": "Explain the role of the transformer architecture in language models."}
]

# Run inference
output = pipe(
    messages,
    max_new_tokens=100,
    temperature=0.6,
    top_p=0.9
)

print(output[0]["generated_text"][-1]["content"])