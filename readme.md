AI/ML Research Agent
This Streamlit application takes a company name, researches it, and generates a PDF report with the top 5 AI/ML use cases that could help the company's growth. It also finds relevant datasets, GitHub repositories, and research papers for each use case.

1. Project Structure
(No changes to the project structure)

2. Local Setup
Step 1 & 2: Clone and Install
(No changes to these steps)

Step 3: Get Your API Keys
You will need credentials for Google, Gemini, Kaggle, and GitHub.

A. Google API Key & Custom Search Engine (CSE) ID

Follow the original instructions to get these two keys from the Google Cloud Console.

B. Gemini API Key

Get this from Google AI Studio.

C. Kaggle API Key

Log into your Kaggle account. Go to https://www.kaggle.com/YOUR_USERNAME/account.

In the API section, click Create New API Token.

This downloads a kaggle.json file. Open it to find your username and key.

D. GitHub Personal Access Token (Recommended)

Go to your GitHub account settings.

Navigate to Developer settings > Personal access tokens > Tokens (classic).

Click Generate new token and select Generate new token (classic).

Give it a descriptive name (e.g., "ResearchAgent").

Set an expiration date (e.g., 90 days).

Under Select scopes, check the box for public_repo. This is all that's needed.

Click Generate token at the bottom and copy the token immediately. You won't be able to see it again.

Step 4: Create and Populate the secrets.toml File
Create the .streamlit/secrets.toml file and add all your keys. It is very important that the names match exactly.

# .streamlit/secrets.toml

# Google Custom Search
GOOGLE_API_KEY = "PASTE_YOUR_GOOGLE_API_KEY_HERE"
GOOGLE_CSE_ID = "PASTE_YOUR_CSE_ID_HERE"

# Google Gemini
GEMINI_API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"

# Kaggle API (from your kaggle.json file)
KAGGLE_USERNAME = "PASTE_YOUR_KAGGLE_USERNAME_HERE"
KAGGLE_KEY = "PASTE_YOUR_KAGGLE_KEY_HERE"

# GitHub API (Personal Access Token)
GITHUB_API_KEY = "PASTE_YOUR_GITHUB_TOKEN_HERE"

Step 5: Run the Application
(No changes to this step)