import os
from bs4 import BeautifulSoup
import requests
import json
from pdf_generator import create_pdf
from github_api import find_github_repos
from arxiv_api import find_arxiv_papers
from kaggle_api import find_kaggle_datasets

try:
    import streamlit as st
except ImportError:
    st = None 

if st and hasattr(st, 'secrets'):
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = st.secrets.get("GOOGLE_CSE_ID")
else:
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def search_google(company_name):
    url = "https://www.googleapis.com/customsearch/v1"
    query = f"about {company_name} business model and products"
    params = {'key': GOOGLE_API_KEY, 'cx': GOOGLE_CSE_ID, 'q': query, 'num': 3}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('items', []), None
    except requests.exceptions.RequestException as e:
        return [], f"Error during Google search: {e}"

def parse_website(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())[:4000], None
    except requests.exceptions.RequestException as e:
        return None, f"Error parsing website {url}: {e}"

def generate_use_cases_with_gemini(company_name, company_info):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""
    Analyze the following information for {company_name} and generate a report for a technical audience.
    Company Information: "{company_info}"

    The report must contain:
    1.  A concise, one-paragraph overview of the company's business model.
    2.  A list of exactly 5 high-impact AI/ML use cases. For each use case, provide:
        - A 'heading'.
        - A detailed 'description'.
        - A list of actionable 'implementation_steps' as a technical guide.

    Return the output ONLY in this exact JSON format, with no extra text or markdown:
    {{
      "overview": "...",
      "use_cases": [
        {{
          "heading": "...", "description": "...", "implementation_steps": ["Step 1: ...", "Step 2: ..."]
        }}
      ]
    }}
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, json=payload, timeout=90)
        response.raise_for_status()
        full_data = response.json()
        json_str = full_data['candidates'][0]['content']['parts'][0]['text']
        clean_json_str = json_str.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_json_str), None
    except (requests.RequestException, json.JSONDecodeError, KeyError, IndexError) as e:
        return {}, f"Error with Gemini API: {e}. Response: {response.text if 'response' in locals() else 'No API response'}"

def process_company_request(company_name):
    """
    Main orchestrator function. It now returns the full data structure for UI display.
    """
    search_results, error = search_google(company_name)
    if error: return None, None, None, None, error
    if not search_results: return None, None, None, None, "Could not find any info for the company."

    company_info = ""
    for result in search_results:
        content, error = parse_website(result['link'])
        if content: company_info += content + " "

    if not company_info: return None, None, None, None, "Could not parse websites; they may block scrapers."

    use_cases_data, error = generate_use_cases_with_gemini(company_name, company_info)
    if error: return None, None, None, None, error
    if not use_cases_data or 'use_cases' not in use_cases_data:
        return None, None, None, None, "AI model returned an unexpected format."

    overview = use_cases_data.get('overview', 'No overview generated.')
    formatted_use_cases = []
    for case in use_cases_data.get('use_cases', []):
        heading = case.get('heading', 'No heading')
        search_query = f"{company_name} {heading}"
        formatted_use_cases.append({
            "heading": heading,
            "description": case.get('description', ''),
            "implementation_steps": case.get('implementation_steps', []),
            "datasets": find_kaggle_datasets(search_query),
            "repos": find_github_repos(search_query),
            "papers": find_arxiv_papers(search_query)
        })

    pdf_bytes = create_pdf(company_name, overview, formatted_use_cases)
    pdf_filename = f"{company_name.replace(' ', '_')}_AI_ML_Report.pdf"
    
    # Return all data for the UI
    return overview, formatted_use_cases, pdf_bytes, pdf_filename, None

