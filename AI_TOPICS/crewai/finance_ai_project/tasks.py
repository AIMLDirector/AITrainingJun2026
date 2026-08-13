from crewai import Task

from agents import (
    market_research_agent,
    valuation_agent,
    investment_advisor_agent
)

market_task = Task(
    description="""
    Analyze the company stock for ticker: {ticker}

    Include:
    - market trends
    - company performance
    - growth opportunities
    - risks
    """,
    agent=market_research_agent,
    expected_output="Detailed market analysis report"
)

valuation_task = Task(
    description="""
    Perform valuation for ticker: {ticker}

    Use:
    - EPS: {eps}
    - PE Ratio: {pe_ratio}
    - Current Price: {current_price}

    Calculate:
    - intrinsic value
    - valuation insights
    - investment attractiveness
    """,
    agent=valuation_agent,
    expected_output="Detailed valuation report"
)

recommendation_task = Task(
    description="""
    Based on market analysis and valuation,
    generate final recommendation for ticker: {ticker}

    Provide:
    - Buy/Sell/Hold
    - Risk level
    - Long-term outlook
    """,
    agent=investment_advisor_agent,
    expected_output="Investment recommendation"
)