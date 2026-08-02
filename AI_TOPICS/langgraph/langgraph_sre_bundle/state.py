
from typing import TypedDict

class IncidentState(TypedDict):
    java_log:str
    infra_log:str
    network_log:str
    java_analysis:dict
    infra_analysis:dict
    network_analysis:dict
    root_cause:str
    recommendation:str
