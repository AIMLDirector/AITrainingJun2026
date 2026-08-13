from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)



def summarize_news(news_text):

    prompt = f"""
    Analyze the following financial news.

    Provide:
    - sentiment
    - risk summary
    - investment insight

    News:
    {news_text}
    """

    response = llm.invoke(prompt)

    return response.content