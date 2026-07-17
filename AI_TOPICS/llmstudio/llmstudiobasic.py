import os
import requests
import json
response = requests.post(
  "http://localhost:1234/api/v1/chat",
  headers={
    "Authorization": f"Bearer 'sk-lm-F6ZGRmyp:hJfex0sZJKTRlpNR1rft'",
    "Content-Type": "application/json"
  },
  json={
    "model": "liquid/lfm2-1.2b",
    "input": "how to work on python code integrating with kafka"
  }
)
print(json.dumps(response.json(), indent=2))