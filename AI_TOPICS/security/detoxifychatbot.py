import os
from dotenv import load_dotenv
from detoxify import Detoxify
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found")

toxicity_model = Detoxify("multilingual")

llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.3
)

THRESHOLDS = {
    "toxicity": 0.50,
    "severe_toxicity": 0.50,
    "obscene": 0.50,
    "threat": 0.50,
    "insult": 0.50,
    "identity_attack": 0.50
}


def check_toxicity(text):
    scores = toxicity_model.predict(text)

    for category, threshold in THRESHOLDS.items():
        if scores.get(category, 0) > threshold:
            return {
                "is_toxic": True,
                "reason": category,
                "scores": scores
            }

    return {
        "is_toxic": False,
        "reason": None,
        "scores": scores
    }


class SecureChatBot:

    def __init__(self):
        self.chat_history = [
            SystemMessage(
                content="You are a helpful AI assistant."
            )
        ]

    def invoke(self, user_input):

        input_check = check_toxicity(user_input)

        if input_check["is_toxic"]:
            return {
                "status": "blocked",
                "reason": input_check["reason"],
                "scores": input_check["scores"]
            }

        self.chat_history.append(
            HumanMessage(content=user_input)
        )

        response = llm.invoke(self.chat_history)

        ai_response = response.content

        output_check = check_toxicity(ai_response)

        if output_check["is_toxic"]:
            return {
                "status": "blocked",
                "reason": f"output_{output_check['reason']}",
                "scores": output_check["scores"]
            }

        self.chat_history.append(
            AIMessage(content=ai_response)
        )

        return {
            "status": "success",
            "response": ai_response,
            "scores": output_check["scores"]
        }


def main():

    chatbot = SecureChatBot()

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        try:

            result = chatbot.invoke(user_input)

            if result["status"] == "blocked":
                print(f"Blocked: {result['reason']}")
            else:
                print(f"Assistant: {result['response']}")

        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    main()