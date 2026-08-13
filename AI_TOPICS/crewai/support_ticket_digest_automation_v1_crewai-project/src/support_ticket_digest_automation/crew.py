import os


from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task







@CrewBase
class SupportTicketDigestAutomationCrew:
    """SupportTicketDigestAutomation crew"""

    
    @agent
    def zendesk_ticket_fetcher(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["zendesk_ticket_fetcher"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            apps=[
                    "zendesk/list_zendesk_tickets",
                    
                    "zendesk/search_zendesk",
                    ],
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def support_ticket_analyst(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["support_ticket_analyst"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def support_report_writer(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["support_report_writer"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    

    
    @task
    def fetch_recent_zendesk_tickets(self) -> Task:
        return Task(
            config=self.tasks_config["fetch_recent_zendesk_tickets"],
            markdown=False,
            
            
        )
    
    @task
    def categorize_and_analyze_tickets(self) -> Task:
        return Task(
            config=self.tasks_config["categorize_and_analyze_tickets"],
            markdown=False,
            
            
        )
    
    @task
    def generate_support_digest_report(self) -> Task:
        return Task(
            config=self.tasks_config["generate_support_digest_report"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the SupportTicketDigestAutomation crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model="openai/gpt-4o-mini"),
        )


