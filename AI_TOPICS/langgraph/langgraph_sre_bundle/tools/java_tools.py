
from langchain.tools import tool

@tool
def analyze_java_log(log:str)->dict:
    if "NullPointerException" in log:
        return {"root":"Application Bug","confidence":0.95}
    return {"root":"Unknown","confidence":0.4}
