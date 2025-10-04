import requests
import xml.etree.ElementTree as ET

def find_arxiv_papers(query):
    """
    Finds the top 3 most relevant papers from ArXiv for a given query.
    """
    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': f'all:"{query}"',
        'start': 0,
        'max_results': 3
    }

    # --- DEBUGGING: Print the exact URL being requested ---
    full_url = requests.Request('GET', url, params=params).prepare().url
    print(f"[ArXiv] Searching with URL: {full_url}")
    # --- END DEBUGGING ---

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        papers = []
        
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', namespace):
            title = entry.find('atom:title', namespace).text.strip()
            paper_url = entry.find('atom:id', namespace).text.strip()
            papers.append({"title": title, "url": paper_url})
            
        # --- DEBUGGING: Print the number of found items ---
        print(f"[ArXiv] Found {len(papers)} papers.")
        # --- END DEBUGGING ---
            
        return papers
        
    except (requests.exceptions.RequestException, ET.ParseError) as e:
        print(f"Error searching ArXiv: {e}")
        return []

