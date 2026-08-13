from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import read_kafka_logs
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

log_analyzer_agent = Agent(
    role="Kafka Log Analyzer",
    description="Analyzes Kafka logs to identify issues and provide insights.",
    goal = "Read Kafka logs and provide a summary of any issues or insights found.",
    backstory="An expert in analyzing Kafka logs, capable of identifying patterns, errors, and providing actionable insights to improve system performance.",
    tools=[read_kafka_logs],
    verbose=True,
    llm="gpt-4o-mini"
)

solution_architect_agent = Agent(
    role="Solution Architect",
    description="Designs solutions based on insights provided by the Kafka Log Analyzer.",
    goal = "Use insights from the Kafka Log Analyzer to design a solution that addresses any identified issues.",
    backstory="An experienced solution architect who can take insights from log analysis and design effective solutions to improve system performance and reliability.",
    tools=[],
    verbose=True,
    llm="gpt-4o-mini"
)