import os
import requests

try:
    import streamlit as st
except ImportError:
    st = None

if st and hasattr(st, 'secrets'):
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = st.secrets.get("GOOGLE_CSE_ID")
else:
    from dotenv import load_dotenv
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def _extract_keywords(query_string):
    """Extracts relevant keywords from a long query string for better search results."""
    # Reduced the stop words list to make the search more lenient
    stop_words = set([
        'a', 'an', 'the', 'in', 'on', 'for', 'with', 'of', 'and', 'to', 'from',
        'using', 'about', 'recommendations', 'top', 'impactful'
    ])
    
    clean_query = ''.join(c for c in query_string if c.isalnum() or c.isspace()).lower()
    words = clean_query.split()
    # Kept the length check to avoid single-letter words
    keywords = [word for word in words if word not in stop_words and len(word) > 1]
    return ' '.join(list(dict.fromkeys(keywords)))

def find_kaggle_datasets(heading):
    """Finds Kaggle datasets using Google Search with extracted keywords."""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("Google API credentials not found. Skipping Kaggle search.")
        return []

    search_query = _extract_keywords(heading)
    print(f"Searching Kaggle with lenient query: '{search_query}'")
    
    url = "https://www.googleapis.com/customsearch/v1"
    query = f"{search_query} site:kaggle.com/datasets"
    params = {'key': GOOGLE_API_KEY, 'cx': GOOGLE_CSE_ID, 'q': query, 'num': 3}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get('items', [])
        return [{'title': item['title'], 'url': item['link']} for item in results]
    except requests.exceptions.RequestException as e:
        print(f"Error searching for datasets: {e}")
        return []

