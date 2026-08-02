
from tools.java_tools import analyze_java_log
from tools.infra_tools import analyze_infra_log
from tools.network_tools import analyze_network_log

def java_node(state):
    state["java_analysis"]=analyze_java_log.invoke(state["java_log"])
    return state

def infra_node(state):
    state["infra_analysis"]=analyze_infra_log.invoke(state["infra_log"])
    return state

def network_node(state):
    state["network_analysis"]=analyze_network_log.invoke(state["network_log"])
    return state

def recommendation_node(state):
    if state["java_analysis"]["root"]=="Application Bug":
        state["root_cause"]="Java NullPointerException"
        state["recommendation"]="Rollback release, fix null checks, add unit tests."
    else:
        state["root_cause"]="Needs investigation"
        state["recommendation"]="Collect more evidence."
    return state
