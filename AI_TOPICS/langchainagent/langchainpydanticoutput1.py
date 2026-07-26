from pydantic import BaseModel, Field
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

class IncidentSummary(BaseModel):
    title: str
    root_cause: str
    impact: str
    resolution: str
    summary : str

agent = create_agent(
    model="gpt-4.1-mini",
    response_format=IncidentSummary
)


input_data = """INCIDENT ID: INC-2026-1045

Title: Payment API Service Outage

Date: 24-June-2026

Severity: SEV-1

Description:
At approximately 09:15 UTC, the Payment API started returning HTTP 500
errors for customer transactions. Multiple alerts were triggered from
Datadog indicating elevated error rates and increased response times.

Investigation:
The on-call engineer reviewed application logs and observed a large
number of database connection timeout exceptions. Further investigation
revealed that a recently deployed reporting service was creating
unbounded database connections, exhausting the PostgreSQL connection
pool used by the Payment API.

Impact:
Customers were unable to complete online payments during the incident.
Approximately 18,500 payment requests were received during the outage,
of which 2,300 failed. The outage impacted customers across North
America and Europe.

Root Cause:
A code deployment introduced a connection leak in the reporting service.
The leaked connections exhausted the shared PostgreSQL connection pool,
causing the Payment API to fail database operations.

Resolution:
The reporting service was rolled back to the previous stable version.
The database connection pool was restarted, and temporary connection
limits were increased. Service health metrics returned to normal within
10 minutes after rollback.

Timeline:
09:15 UTC - First alerts triggered
09:18 UTC - Incident declared
09:25 UTC - Root cause identified
09:32 UTC - Rollback initiated
09:40 UTC - Service restored
09:50 UTC - Monitoring confirmed stability

Action Items:
1. Implement connection pool monitoring alerts.
2. Add automated load testing before production deployments.
3. Introduce database connection leak detection.
4. Update deployment runbooks."""

# user_input = input("Enter the incident details: ")
result = agent.invoke({
    "messages": [{"role": "user", "content": input_data}]
})

print(result["structured_response"])
