import requests
from tavily import TavilyClient
import xml.etree.ElementTree as ET
import os

session = requests.Session()
session.headers.update(
    {"User-Agent": "LF-ADP-Agent/1.0 (mailto:your.email@example.com)"}
)


os.environ["TAVILY_API_KEY"] = "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"

def arxiv_search_tool(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches arXiv for research papers matching the given query.
    """
    url = f"https://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"

    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return [{"error": str(e)}]

    try:
        root = ET.fromstring(response.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        results = []
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            authors = [
                author.find("atom:name", ns).text
                for author in entry.findall("atom:author", ns)
            ]
            published = entry.find("atom:published", ns).text[:10]
            url_abstract = entry.find("atom:id", ns).text
            summary = entry.find("atom:summary", ns).text.strip()

            link_pdf = None
            for link in entry.findall("atom:link", ns):
                if link.attrib.get("title") == "pdf":
                    link_pdf = link.attrib.get("href")
                    break

            results.append(
                {
                    "title": title,
                    "authors": authors,
                    "published": published,
                    "url": url_abstract,
                    "summary": summary,
                    "link_pdf": link_pdf,
                }
            )

        return results
    except Exception as e:
        return [{"error": f"Parsing failed: {str(e)}"}]



# Create a session if you haven't already

# Test with a simple query


# results = arxiv_search_tool("quantum computing", max_results=3)

# # Print results
# for i, paper in enumerate(results, 1):
#     if "error" in paper:
#         print(f"Error: {paper['error']}")
#     else:
#         print(f"\n{i}. {paper['title']}")
#         print(f"   Authors: {', '.join(paper['authors'][:3])}")
#         print(f"   Published: {paper['published']}")
#         print(f"   URL: {paper['url']}")
#         print(f"   PDF: {paper['link_pdf']}")
#         print(f"   Summary: {paper['summary'][:150]}...")



## Define the function to be used by agents
arxiv_tool_def = {
    "type": "function",
    "function": {
        "name": "arxiv_search_tool",
        "description": "Searches for research papers on arXiv by query string.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keywords for research papers.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return.",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
}


def tavily_search_tool(
    query: str, max_results: int = 5, include_images: bool = False
) -> list[dict]:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables.")

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    try:
        response = client.search(
            query=query,
            max_results=max_results,
            include_images=include_images,
        )

        results = [
            {
                "title": r.get("title", ""),
                "content": r.get("content", ""),
                "url": r.get("url", ""),
            }
            for r in response.get("results", [])
        ]

        if include_images:
            results.extend(
                {"image_url": img_url}
                for img_url in response.get("images", [])
            )

        return results

    except Exception as e:
        return [{"error": str(e)}]


# results = tavily_search_tool("retrieval augmented generation")
# print(results)


tavily_tool_def = {
    "type": "function",
    "function": {
        "name": "tavily_search_tool",
        "description": "Performs a general-purpose web search using the Tavily API.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keywords for retrieving information from the web.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return.",
                    "default": 5,
                },
                "include_images": {
                    "type": "boolean",
                    "description": "Whether to include image results.",
                    "default": False,
                },
            },
            "required": ["query"],
        },
    },
}



 ## to have a clean text
def parse_input(text_or_messages):
    if isinstance(text_or_messages, list):
        text_report = None
        for m in reversed(text_or_messages):
            role = m.get("role") if isinstance(
                m, dict) else getattr(m, "role", None)
            content = (
                m.get("content") if isinstance(
                    m, dict) else getattr(m, "content", None)
            )
            if role == "assistant" and content:
                text_report = content
                break
        if not text_report:
            raise ValueError("No assistant text found in messages.")

    else:
        text_report = str(text_or_messages)

    return text_report
