from tavily import TavilyClient
import os

# The client automatically picks up the TAVILY_API_KEY environment variable
# or you can pass it directly: TavilyClient(api_key="tvly-YOUR_API_KEY")
tavily_client = TavilyClient()

response = tavily_client.search("Who is Leo Messi?")

# Print the response (which is a dictionary)
print(response)

# Accessing specific snippets/results
for result in response.get("results", []):
    print(f"Content: {result['content']}")
    print(f"Source: {result['url']}")
