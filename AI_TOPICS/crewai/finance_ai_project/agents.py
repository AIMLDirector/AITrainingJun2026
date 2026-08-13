from crewai import Agent
from dotenv import load_dotenv
load_dotenv()
market_research_agent = Agent(
    role="Market Research Analyst",
    goal="Analyze stock market trends and company performance",
    backstory="Expert financial analyst with experience in stock research",
    verbose=True
)


valuation_agent = Agent(
    role="Valuation Expert",
    goal="Calculate intrinsic value and financial ratios",
    backstory="Experienced CFA valuation specialist",
    verbose=True
)


investment_advisor_agent = Agent(
    role="Investment Advisor",
    goal="Generate investment recommendations",
    backstory="AI-powered investment strategist",
    verbose=True
)