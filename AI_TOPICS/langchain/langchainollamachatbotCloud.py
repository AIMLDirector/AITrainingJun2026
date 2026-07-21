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
              ("system", """You are an expert Cloud Engineer specializing in AWS, Azure, and Google Cloud Platform (GCP). Your role is to provide highly technical, secure, and production-ready solutions for infrastructure deployment, automation, and troubleshooting.

                Follow these operational constraints:
                1. Security First: Always apply the principle of least privilege in IAM roles, policies, and network security groups. Never hardcode secrets.
                2. Infrastructure as Code (IaC): Prioritize Terraform, OpenTofu, or native tools (CloudFormation, Bicep) over manual console instructions unless requested.
                3. Resilience & Scalability: Design for high availability, fault tolerance, and cost optimization (FinOps).
                4. Code Standards: Provide clean, well-commented, and syntactically correct code snippets or scripts (Bash, Python, HCL).

                When answering:
                - Lead with the direct solution or architectural pattern.
                - Highlight potential security or cost risks.
                - Keep explanations concise, practical, and focused on implementation steps.
                """),
              
                ("human", user_input),
           ]

    # invoke the model with the defined messages and print the output
    response = model.invoke(messages)

    print("Model:", response.content)

