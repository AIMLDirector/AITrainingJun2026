from tavily import TavilyClient

tavily_client = TavilyClient(api_key="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")
response = tavily_client.search("What are the latest developments in AI?")

print(response["results"][2]["content"])