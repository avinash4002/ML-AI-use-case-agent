import os
import requests
import json
from dotenv import load_dotenv

# --- Instructions ---
# 1. Make sure you have a .env file in the same directory as this script.
# 2. Your .env file should contain your Gemini API key like this:
#    GEMINI_API_KEY="AIzaSy..."
# 3. Run this script from your terminal: python check_models.py
# 4. Look for a model in the output that supports the "generateContent" method.
# 5. Update the model name in your utils.py file with one from the list.
#    For example, if you see 'models/gemini-pro', update the URL in utils.py.

def list_available_models():
    """
    Calls the Gemini API to list all available models and their supported methods.
    """
    # Load the API key from the .env file
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

    print("Fetching available models...")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        models_data = response.json()
        
        print("\n--- Available Gemini Models ---")
        for model in models_data.get('models', []):
            display_name = model.get('displayName', 'N/A')
            model_name = model.get('name', 'N/A')
            supported_methods = model.get('supportedGenerationMethods', [])
            
            print(f"\nModel Name: {model_name}")
            print(f"  Display Name: {display_name}")
            print(f"  Supported Methods: {', '.join(supported_methods)}")
        
        print("\n---------------------------------")
        print("\nFind a model that supports 'generateContent' and update your utils.py file.")

    except requests.exceptions.RequestException as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your API key and network connection.")
    except json.JSONDecodeError:
        print("\nError: Could not decode the response from the API.")

if __name__ == "__main__":
    list_available_models()
