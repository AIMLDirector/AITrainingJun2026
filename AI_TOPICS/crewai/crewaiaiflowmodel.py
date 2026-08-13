import os
from typing import List
from pydantic import BaseModel, Field
# Added LLM to imports
from crewai import Agent, Task, Crew, Process, LLM
from crewai.flow.flow import Flow, listen, router, start, or_
from dotenv import load_dotenv
load_dotenv()
# cloud_llm = LLM(model="anthropic/claude-3-5-sonnet")
# qwen_llm = LLM(model="tencent/qwen-2.5", base_url="http://localhost:11434")

# openai/google|qwen  - ( server, platform , application)
# anthropic - end user ( laptop, linkedin, github,  security laptop , security analyst,)

# cloud_llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")

# 1. Define Model and API Keys
# Make sure your environment variable is set: export OPENAI_API_KEY="your-key"
cloud_llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.2 # Lower temperature for analytical deterministic logs
)

class LogAnalyticsState(BaseModel):
    raw_log_dump: str = ""
    incident_severity: str = "LOW"
    root_cause_summary: str = ""

class CloudLogObservabilityFlow(Flow[LogAnalyticsState]):

    @start()
    def ingest_cloud_logs(self):
        print("Ingesting recent raw cloud logs...")
        self.state.raw_log_dump = """
        2026-05-28T20:31:02Z [WARN] PaymentService: DB pool connection retry 1/3...
        2026-05-28T20:31:05Z [FATAL] OrderProcessingService: java.lang.OutOfMemoryError: Java heap space. Exiting thread.
        2026-05-28T20:31:06Z [ERROR] GatewayService: Upstream 502 Bad Gateway while routing to /orders
        """
        print("Logs mapped to pipeline storage.")

    @router(ingest_cloud_logs)
    def assess_severity_and_route(self):
        print("Scanning logs for critical runtime exceptions...")
        logs = self.state.raw_log_dump.upper()
        if "FATAL" in logs or "OUTOFMEMORYERROR" in logs:
            self.state.incident_severity = "CRITICAL"
            return "critical_incident_detected"
        elif "ERROR" in logs:
            self.state.incident_severity = "MEDIUM"
            return "standard_incident_detected"
        else:
            return "system_healthy"

    @listen("critical_incident_detected")
    def run_deep_diagnostic_crew(self):
        print("Assembling Site Reliability Engineering (SRE) Agents...")

        # 2. Assign the LLM configuration explicitly to each Agent
        log_parser = Agent(
            role="Cloud Infrastructure Log Parser",
            goal="Isolate specific stack traces and contextual patterns from raw log streams.",
            backstory="An automated expert agent trained to clean noise from production streams.",
            llm=cloud_llm, # Passed here
            verbose=True
        )

        root_cause_analyst = Agent(
            role="Principal Site Reliability Engineer (SRE)",
            goal="Identify the technical root cause and outline an immediate path to system remediation.",
            backstory="A battle-tested cloud architect skilled at debugging distributed system failures.",
            llm=cloud_llm, # Passed here
            verbose=True
        )

        parse_task = Task(
            description=f"Filter and isolate the exact timestamps, services, and stack traces inside these logs: {self.state.raw_log_dump}",
            expected_output="A structured list of localized service exceptions and cascading errors.",
            agent=log_parser
        )

        diagnosis_task = Task(
            description="Analyze the parsed service errors. Provide a clear, technical Root Cause Analysis (RCA) and concrete mitigation actions.",
            expected_output="An operational incident write-up detailing the core problem and exactly how to fix it.",
            agent=root_cause_analyst
        )

        sre_crew = Crew(
            agents=[log_parser, root_cause_analyst],
            tasks=[parse_task, diagnosis_task],
            process=Process.sequential
        )
        
        # 3. The Crew will execute and make API calls to the LLM here
        crew_output = sre_crew.kickoff()
        self.state.root_cause_summary = str(crew_output)
        print("Root cause investigation completed successfully.")

    @listen(or_("standard_incident_detected", "run_deep_diagnostic_crew"))
    def dispatch_incident_report(self):
        print("\n================== DISPATCHING INCIDENT REPORT ==================")
        print(f"Severity Classification: [{self.state.incident_severity}]")
        print("\n--- Diagnostic Investigation Details ---")
        print(self.state.root_cause_summary if self.state.root_cause_summary else "Standard warning telemetry captured.")
        return self.state.root_cause_summary

if __name__ == "__main__":
    observability_pipeline = CloudLogObservabilityFlow()
    observability_pipeline.kickoff()
