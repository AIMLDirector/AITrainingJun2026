
from langchain.tools import tool

@tool
def analyze_infra_log(log:str)->dict:
    if "CPU" in log:
        return {"cpu":"high"}
    return {"cpu":"normal"}
