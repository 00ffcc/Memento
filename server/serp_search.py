from serpapi import GoogleSearch
from mcp.server.fastmcp import FastMCP
import json
import os

# --------------------------------------------------------------------------- #
#  FastMCP server instance
# --------------------------------------------------------------------------- #

mcp = FastMCP("serpapi")

# --------------------------------------------------------------------------- #
#  Tools
# --------------------------------------------------------------------------- #

# 加入搜索结果缓存
search_cache = {}
with open("cache_search_results.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        query = data["query"]
        results = data["results"]
        search_cache[query] = results

@mcp.tool()
async def google_search(query: str) -> list[dict]:
    """
    Run a Google search via SerpAPI and return the organic results.
    
    Parameters
    ----------
    query : str
        The search query string (e.g., "Coffee")
    
    Returns
    -------
    list[dict]
        The list of organic search results from Google.
    """
    if query in search_cache:
        return search_cache[query]
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY")  # please set your api key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    search_cache[query] = results.get("organic_results", [])
    with open("cache_search_results.jsonl", "a", encoding="utf-8") as f:
        json.dump({"query": query, "results": results.get("organic_results", [])}, f, ensure_ascii=False)
        f.write("\n")

    return results.get("organic_results", [])

# --------------------------------------------------------------------------- #
#  Entrypoint
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    mcp.run(transport="stdio")
