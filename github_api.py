import os
import requests

try:
    import streamlit as st
except ImportError:
    st = None

# Use secrets from Streamlit if available, otherwise use environment variables
if st and hasattr(st, 'secrets'):
    GITHUB_API_KEY = st.secrets.get("GITHUB_API_KEY")
else:
    from dotenv import load_dotenv
    load_dotenv()
    GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

def _extract_keywords(query_string):
    """Extracts relevant keywords from a long query string for a lenient search."""
    # Drastically reduced stop words for a more lenient search
    stop_words = set(['a', 'an', 'the', 'in', 'on', 'for', 'with', 'of', 'and', 'to', 'from', 'using'])
    
    clean_query = ''.join(c for c in query_string if c.isalnum() or c.isspace()).lower()
    words = clean_query.split()
    # Lowered character limit to include more potential keywords
    keywords = [word for word in words if word not in stop_words and len(word) > 1]
    
    # Using " OR " (must be capitalized) makes the search much more lenient
    return ' OR '.join(list(dict.fromkeys(keywords)))

def find_github_repos(heading):
    """Finds top GitHub repositories based on extracted keywords from the use case heading."""
    if not GITHUB_API_KEY:
        print("GitHub API key not found. Skipping GitHub search.")
        return []

    search_query = _extract_keywords(heading)
    # If the query is empty after filtering, fall back to a general search term
    if not search_query.strip():
        search_query = "machine learning"
        
    print(f"Searching GitHub with lenient query: '{search_query}'")
    
    url = "https://api.github.com/search/repositories"
    headers = {'Authorization': f'token {GITHUB_API_KEY}'}
    params = {'q': search_query, 'sort': 'stars', 'order': 'desc', 'per_page': 3}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json().get('items', [])
        return [{
            'name': repo.get('full_name'),
            'url': repo.get('html_url'),
            'stars': repo.get('stargazers_count', 0)
        } for repo in results]
    except requests.exceptions.RequestException as e:
        print(f"Error searching GitHub: {e}")
        return []

