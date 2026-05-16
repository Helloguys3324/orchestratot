"""
Web Search Skill — Search the web using httpx.
"""
import httpx


async def web_search(query: str, num_results: int = 5) -> str:
    """Search the web and return results."""
    try:
        url = "https://www.google.com/search"
        params = {"q": query, "num": num_results}
        headers = {"User-Agent": "Mozilla/5.0"}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, headers=headers)
            return f"Search results for '{query}': Status {resp.status_code}"
    except Exception as e:
        return f"Search error: {str(e)}"
