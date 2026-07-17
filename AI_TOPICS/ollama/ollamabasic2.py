from ollama import chat

response = chat(
    model="wen3.5:2b",
    messages=[
        {"role": "system", "content": '''You are a Senior Data Engineering Expert with 15+ years of experience designing, building, and optimizing data platforms.'''},
        {"role": "user", "content": "Explain ETL vs ELT."}
    ]

)

print(response["message"]["content"])


while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Exiting the chat.")
        break

    response = chat(
        model="qwen3-vl:8b",
        messages=[
            {"role": "system", "content": '''You are a  Senior Java Developer and SME with 15+ years of experience designing, building, and optimizing Java applications.'''},
            {"role": "user", "content": user_input}
        ]
    )

    print("AI:", response["message"]["content"])