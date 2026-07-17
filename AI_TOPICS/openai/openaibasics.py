from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
client = OpenAI()

response = client.responses.create(
    model="gpt-5.4-nano",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)

