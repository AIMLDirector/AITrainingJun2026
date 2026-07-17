from ollama import chat

response = chat(
  model='qwen3.5:2b',
  messages=[{'role': 'user', 'content': 'How many letter r are in strawberry?'}],
  think=True,
  stream=False,
)

print('Thinking:\n', response.message.thinking)
print('Answer:\n', response.message.content)