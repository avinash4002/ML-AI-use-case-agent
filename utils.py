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
        error_message = f"Error during Google search: {e}"
        print(error_message)
        return [], error_message

def parse_website(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            script_or_style.decompose()
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())[:4000], None
    except requests.exceptions.RequestException as e:
        error_message = f"Error parsing website {url}: {e}"
        print(error_message)
        return None, error_message

def generate_use_cases_with_gemini(company_name, company_info):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""
    Based on the information about {company_name}, generate a report for a technical audience.
    Company Information: "{company_info}"

    The report must contain:
    1. A brief, one-paragraph overview of the company's business model.
    2. A list of 5 AI/ML use cases. For each use case, provide:
       - A 'heading'.
       - A 'description'.
       - A list of 'implementation_steps' as a technical guide.

    Return the output ONLY in this exact JSON format:
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
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        full_data = response.json()
        # More robust parsing of the Gemini response
        try:
            json_str = full_data['candidates'][0]['content']['parts'][0]['text']
            # Clean potential markdown formatting from the JSON string
            clean_json_str = json_str.strip().replace("```json", "").replace("```", "")
            return json.loads(clean_json_str), None
        except (KeyError, IndexError, json.JSONDecodeError) as parse_error:
            error_message = f"Could not parse JSON from Gemini response: {parse_error}. Raw response: {full_data}"
            print(error_message)
            return {}, error_message
            
    except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError) as e:
        error_message = f"Error interacting with Gemini API: {e}. Response: {response.text if 'response' in locals() else 'No response'}"
        print(error_message)
        return {}, error_message

def process_company_request(company_name):
    search_results, error = search_google(company_name)
    if error:
        return None, None, error
    if not search_results:
        return None, None, "Could not find any information about the company. Please try a different name."

    company_info = ""
    for result in search_results:
        content, error = parse_website(result['link'])
        if error:
            print(f"Skipping a link due to parsing error: {error}") # Log but don't stop
        if content:
            company_info += content + " "
    
    if not company_info:
        return None, None, "Could not parse content from any of the found websites. They may be blocking scrapers."

    use_cases_data, error = generate_use_cases_with_gemini(company_name, company_info)
    if error:
        return None, None, error
    if not use_cases_data or 'use_cases' not in use_cases_data:
        return None, None, "The AI model returned an unexpected format. Could not extract use cases."

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

    pdf_bytes = create_pdf(
        company_name,
        use_cases_data.get('overview', 'No overview generated.'),
        formatted_use_cases
    )
    
    pdf_filename = f"{company_name.replace(' ', '_')}_AI_ML_Report.pdf"
    return pdf_bytes, pdf_filename, None

