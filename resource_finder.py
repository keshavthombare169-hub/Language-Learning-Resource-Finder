"""
Agent 1 — Resource Finder
Uses Tavily Search (free tier: 1000 searches/month) to find real,
current language learning resources on the internet.
"""
import os
import requests
from llm import call_gemini

TAVILY_API_URL = "https://api.tavily.com/search"

SYSTEM_PROMPT = """You are the Resource Finder agent for a language learning assistant.

You will receive:
1. A target language and level
2. Real web search results from Tavily Search

Your job:
- Analyze the search results
- Identify the best apps, YouTube channels, podcasts, and courses from the results
- For each resource, write: name, type, why it suits this level, and where to find it
- List exactly 6 resources (2 apps, 2 YouTube channels, 2 podcasts/courses)
- Be concise: 2–3 lines per resource

Format each resource like:
**[Name]** (Type)
Why it's great: ...
Find it: ...
"""

def tavily_search(query: str, max_results: int = 8) -> list[dict]:
    """Call Tavily Search API and return results."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY not set. "
            "Get a free key at https://app.tavily.com"
        )
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
        "include_answer": False,
    }
    resp = requests.post(TAVILY_API_URL, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json().get("results", [])


def resource_finder_agent(language: str, level: str) -> tuple[str, list]:
    """
    Search the web for language learning resources,
    then use Gemini to synthesize them into a clean list.

    Returns:
        (formatted_resources_str, raw_tavily_results)
    """
    query = f"best {language} learning resources {level.lower()} {language} apps YouTube podcasts courses 2024"
    tavily_results = tavily_search(query)

    search_context = "\n\n".join([
        f"Title: {r.get('title', '')}\nURL: {r.get('url', '')}\nSnippet: {r.get('content', '')[:300]}"
        for r in tavily_results
    ])

    user_message = f"""Target language: {language}
Level: {level}

Web search results from Tavily:
{search_context}

Please identify and list the 6 best learning resources from these results."""

    result = call_gemini(SYSTEM_PROMPT, user_message)
    return result, tavily_results
