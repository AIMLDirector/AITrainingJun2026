from langchain_ollama import ChatOllama

# initialize the ChatOllama model with the specified parameters
model = ChatOllama(
          model="qwen3-vl:8b",
          validate_model_on_init=True,
          temperature=0.8)



while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    # define the messages to be sent to the model with system and human role 
    messages = [
              ("system", "You are a helpful translator. Translate the user sentence to French."),
              ("human", user_input),
           ]

    # invoke the model with the defined messages and print the output
    response = model.invoke(messages)

    print("Model:", response.content)

