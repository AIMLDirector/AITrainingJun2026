
from langchain.tools import tool

@tool
def analyze_network_log(log:str)->dict:
    if "Packet Loss" in log:
        return {"network":"degraded"}
    return {"network":"healthy"}
