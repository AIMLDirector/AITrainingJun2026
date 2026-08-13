from crewai import Task
from agents import log_analyzer_agent, solution_architect_agent

analyze_kafka_logs_task = Task(
    description="""
    Analyze the Kafka log file located at:

    {log_file_path}

    Extract:
    - Key issues
    - Error patterns
    - Warnings
    - Insights
    - Root causes
    - Recommendations

    Use the kafka_log_analyzer tool to read the logs.
    """,

    agent=log_analyzer_agent,

    expected_output="""
    Structured Kafka log analysis report including:
    - Critical issues
    - Warning summary
    - Root cause analysis
    - Operational insights
    - Recommendations
    """
)

solution_task = Task(
    description="""
    Based on the Kafka log analysis results,
    design a long-term scalable solution.

    Include:
    - Architecture improvements
    - Monitoring recommendations
    - Scaling recommendations
    - Kafka tuning suggestions
    - SRE best practices
    - Automation opportunities
    - Useful implementation resources
    """,

    agent=solution_architect_agent,

    expected_output="""
    Strategic long-term Kafka reliability and scalability solution
    with implementation recommendations and reference resources.
    """
)
