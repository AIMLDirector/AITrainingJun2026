
from graph import graph

state={
"java_log":"java.lang.NullPointerException at PaymentController.java:84",
"infra_log":"CPU 98%",
"network_log":"Packet Loss 40%"
}

result=graph.invoke(state)
print("\nRoot Cause:",result["root_cause"])
print("Recommendation:",result["recommendation"])
print("Java:",result["java_analysis"])
print("Infra:",result["infra_analysis"])
print("Network:",result["network_analysis"])
