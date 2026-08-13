from crewai.tools import tool

@tool("kakfa_log_analyzer")
def read_kafka_logs(log_file_path: str):
    """Read Kafka logs from the specified file path and return the content as a string."""
    try:
        with open(log_file_path, 'r') as file:
            logs = file.read()
            return logs
    except Exception as e:
        return f"Error reading Kafka logs: {str(e)}"

