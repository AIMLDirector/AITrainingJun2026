from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
load_dotenv()

progammer = Agent(
    name="Progammer",
    role= "python developer",
    goal="Write and execute python code to solve the user problem",
    backstory="You are an expert coder with experience in various programming languages and frameworks. You have a strong understanding of algorithms and data structures, and you are skilled at debugging and optimizing code. Your primary focus is to write efficient and effective code to solve the user's problem.",
    allow_code_execution=False,
    Verbose=True

)

work_assignment = Task(
    name="Work Assignment",
    description="write a code end to end for the requested python functionality",
    expected_output="The task should be assigned to the Progammer agent, as they have the necessary skills and experience to write and execute python code to solve the user's problem, give a explanation about the code also",
    agent= progammer

)

crew = Crew(
    agents = [progammer],
    tasks= [work_assignment],
    process = Process.sequential,
    Tracing = True
)

user_input  = input("Enter your problem statement: ")
Result = crew.kickoff(inputs={"problem_statement": user_input})
print(Result)