from crewai.tools import tool
from tavily import TavilyClient
import os

@tool("web_search")
def web_search(query: str) -> str:
    """Web search tool to gain information of a topic online based on the input query"""
    tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query = query,
        search_depth = "advanced",
        max_results = 3
    )
    res = ''
    for i,result in enumerate(response['results']):
        res += f"Website {i+1}:\n" + result["content"] + "\n\n"
    return res