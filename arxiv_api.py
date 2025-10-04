import requests
import xml.etree.ElementTree as ET

def _extract_keywords(query_string):
    """Extracts relevant keywords from a long query string for a lenient search."""
    # Drastically reduced stop words for a more lenient search
    stop_words = set(['a', 'an', 'the', 'in', 'on', 'for', 'with', 'of', 'and', 'to', 'from', 'using'])
    
    clean_query = ''.join(c for c in query_string if c.isalnum() or c.isspace()).lower()
    words = clean_query.split()
    # Lowered character limit to include more potential keywords
    keywords = [word for word in words if word not in stop_words and len(word) > 1]
    
    # Using "OR" makes the search much more lenient, returning papers that match any keyword.
    return ' OR '.join(list(dict.fromkeys(keywords)))

def find_arxiv_papers(heading):
    """Searches ArXiv for papers based on extracted keywords."""
    search_query = _extract_keywords(heading)
    # If for some reason the query is empty, search for a general term.
    if not search_query.strip():
        search_query = "machine learning"
        
    print(f"Searching ArXiv with lenient query: '{search_query}'")

    url = "http://export.arxiv.org/api/query"
    params = {'search_query': f'all:{search_query}', 'start': 0, 'max_results': 3}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            url = entry.find('{http://www.w3.org/2005/Atom}id').text.strip()
            papers.append({'title': title, 'url': url})
        return papers
    except (requests.exceptions.RequestException, ET.ParseError) as e:
        print(f"Error searching ArXiv: {e}")
        return []

