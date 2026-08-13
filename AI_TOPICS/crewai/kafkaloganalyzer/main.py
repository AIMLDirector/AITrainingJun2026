from crewai import Crew
from tasks import analyze_kafka_logs_task, solution_task
import os


def run_kafka_analyzer():
    crew = Crew(
        name="Kafka Log Analysis Crew",
        description="A crew of agents that analyze Kafka logs and design solutions based on the analysis.",
        tasks=[analyze_kafka_logs_task, solution_task],
        verbose=True
    )

    input_file = input("Enter the path to the Kafka log file: ")

    if not os.path.exists(input_file):
        print("Log file does not exist!")
        return

    result = crew.kickoff(
        inputs={
            "log_file_path": input_file
        }
    )

    print("Final Result:")
    print(result)


if __name__ == "__main__":
    run_kafka_analyzer()



if __name__ == "__main__":
    run_kafka_analyzer()