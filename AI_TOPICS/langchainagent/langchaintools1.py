from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

import requests
from bs4 import BeautifulSoup

load_dotenv()


class AWSDocumentResponse(BaseModel):
    """Structured AWS documentation response"""

    topic: str = Field(description="AWS topic requested")
    summary: str = Field(description="Summary of the AWS documentation")
    commands: list[str] = Field(description="AWS CLI commands")
    important_notes: list[str] = Field(description="Important notes")


@tool
def search_aws_docs(query: str) -> str:
    """
    Search AWS documentation and return content.
    """

    search_url = (
        f"https://docs.aws.amazon.com/search/doc-search.html?"
        f"searchPath=documentation-guide&searchQuery={query}"
    )

    try:
        response = requests.get(
            search_url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code != 200:
            return f"AWS documentation search failed: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:5000]

    except Exception as e:
        return f"Error searching AWS docs: {str(e)}"


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[search_aws_docs],
    response_format=AWSDocumentResponse,
    system_prompt="""
You are an AWS Solutions Architect.

When users ask AWS questions:

1. Use search_aws_docs tool.
2. Extract useful information.
3. Return:
   - topic
   - summary
   - commands
   - important_notes
"""
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "How do I create an S3 bucket using AWS CLI?"
            }
        ]
    }
)

print("\n===== Structured Response =====\n")
print(result["structured_response"])