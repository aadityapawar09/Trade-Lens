import os
from tavily import TavilyClient


def get_news(company_name):
    # Search the web for recent financial news about the company
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        result = client.search(
            company_name + " stock financial news", topic="news", max_results=5
        )
    except Exception as error:
        print("News search problem:", error)
        return []  # an empty list means "no news found"

    # Keep only the headline (title) of each news result
    headlines = []
    for item in result["results"]:
        headlines.append(item["title"])
    return headlines
