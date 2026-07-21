from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# initialize the ChatOpenAI model with the specified parameters
model = ChatOpenAI(
            model="gpt-5.4-nano",
            temperature=0.8,
            max_tokens=1000,
            top_p=0.9)

# define the messages to be sent to the model with system and human role 
messages = [
          ("system", "You are a helpful translator. Translate the user sentence to French."),
          ("human", "I love programming."),
       ]

# invoke the model with the defined messages and print the output
response = model.invoke(messages)

print(response.content)