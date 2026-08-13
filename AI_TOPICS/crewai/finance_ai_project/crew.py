from crewai import Crew

from tasks import (
    market_task,
    valuation_task,
    recommendation_task
)


finance_crew = Crew(
    agents=[],
    tasks=[
        market_task,
        valuation_task,
        recommendation_task
    ],
    verbose=True
)