
import os
import requests

try:
    import streamlit as st
    # Use a specific key for GitHub for better management
    GITHUB_API_KEY = st.secrets.get("GITHUB_API_KEY", None)
except (ImportError, KeyError):
    from dotenv import load_dotenv
    load_dotenv()
    GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

def find_github_repos(query):
    """
    Finds the top 3 relevant GitHub repositories for a given query.
    Uses a GitHub Personal Access Token if available for higher rate limits.
    """
    print(f"Searching GitHub for: '{query}'")
    url = "https://api.github.com/search/repositories"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    # If a GitHub token is provided, use it for authentication
    if GITHUB_API_KEY:
        headers["Authorization"] = f"token {GITHUB_API_KEY}"
        print("Using GitHub API Key for authentication.")

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 3
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        repos = []
        for item in data.get("items", []):
            repos.append({
                "name": item["full_name"],
                "url": item["html_url"],
                "stars": item["stargazers_count"]
            })
        print(f"Found {len(repos)} GitHub repos.")
        return repos
    except requests.exceptions.RequestException as e:
        print(f"Error searching GitHub: {e}")
        return []

