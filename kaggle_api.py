import os
import requests

# --- API Configuration ---
try:
    import streamlit as st
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    GOOGLE_CSE_ID = st.secrets["GOOGLE_CSE_ID"]
except (ImportError, KeyError):
    from dotenv import load_dotenv
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def find_kaggle_datasets(query):
    """
    Finds the top 3 Kaggle datasets using Google Custom Search.
    """
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("Error: Google API Key or CSE ID not found for Kaggle search.")
        return []
        
    search_query = f"site:kaggle.com/datasets {query}"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CSE_ID,
        'q': search_query,
        'num': 3
    }
    
    # --- DEBUGGING: Print the exact URL being requested ---
    full_url = requests.Request('GET', url, params=params).prepare().url
    print(f"[Kaggle] Searching with URL: {full_url}")
    # --- END DEBUGGING ---

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json().get('items', [])
        
        # --- DEBUGGING: Print the number of found items ---
        print(f"[Kaggle] Found {len(search_results)} datasets.")
        # --- END DEBUGGING ---

        return [
            {"title": item.get('title', 'N/A'), "url": item.get('link')} 
            for item in search_results
        ]

    except requests.exceptions.RequestException as e:
        print(f"Error searching for Kaggle datasets: {e}")
        return []

