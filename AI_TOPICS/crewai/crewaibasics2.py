import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, PDFSearchTool
load_dotenv()
search_tool = SerperDevTool()
pdf_tool = PDFSearchTool(
    pdf="/Users/premkumargontrand/AITrainingMay2026/AIBasics/data/LLMarchitecture.pdf"
)
# 1. Define your Agents
researcher = Agent(
  role='Senior Research Analyst',
  goal='Uncover cutting-edge developments in {topic}',
  backstory="""You are a senior AI researcher.
    Always search the web first to find the latest
    developments before answering.

    Then compare your findings with the PDF.

    Never rely only on your internal knowledge.""",
  tools=[search_tool,pdf_tool ],
  verbose=True,
  allow_delegation=False
)

writer = Agent(
  role='Tech Content Strategist',
  goal='Craft a compelling blog post about {topic}',
  backstory="""You take raw research data and turn it into 
  engaging, easy-to-read articles for a tech audience.""",
  verbose=True
)

research_task= Task(
      description='Analyze the current state of {topic}. Focus on 3 key breakthroughs.',
      expected_output='A detailed list of 3 bullet points with supporting evidence.',
      agent=researcher,
      human_input=True
    )

write_task = Task(
  description='Using the research provided, write a 300-word blog post.',
  expected_output='A markdown formatted blog post.',
  agent=writer,
  context=[research_task] ,
  human_input=True
)


crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential, 
  verbose=True
)


result = crew.kickoff(inputs={'topic': 'AI Agents in Production'})
print(result)
