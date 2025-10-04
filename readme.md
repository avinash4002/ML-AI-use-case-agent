Deployed Project Link: https://ml-ai-use-case-agent-pcgvzbfrs4r9rz3zqo5wbd.streamlit.app/

AI/ML Research Agent
This Streamlit application helps you discover AI/ML use cases to accelerate a company's growth. Enter a company name, and the agent will generate a report with a company overview, top 5 AI/ML use case recommendations, and relevant learning resources.

⚙️ Local Setup Instructions
1. Clone the Repository
Clone this project to your local machine.

2. Install Dependencies
Navigate to the project directory and install the required Python packages:

pip install -r requirements.txt

3. Create a Secrets File
Streamlit uses a specific file to manage secret keys locally. Create a new folder named .streamlit in your main project directory. Inside this new folder, create a file named secrets.toml.

Your project structure should look like this:

- Research_agent/
  - .streamlit/
    - secrets.toml
  - app.py
  - utils.py
  - pdf_generator.py
  - ... (other .py files)
  - requirements.txt

4. Add Your API Keys
Open the secrets.toml file and add your API keys in the following format. Do not use quotes around the keys.

# .streamlit/secrets.toml

# Google API Keys (for company search)
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"
GOOGLE_CSE_ID = "YOUR_GOOGLE_CUSTOM_SEARCH_ENGINE_ID_HERE"

# Gemini API Key (for generating use cases)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# GitHub API Key (for finding repositories)
GITHUB_API_KEY = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN_HERE"

# Kaggle API Credentials (for finding datasets)
KAGGLE_USERNAME = "YOUR_KAGGLE_USERNAME"
KAGGLE_KEY = "YOUR_KAGGLE_API_KEY"

5. Run the Application
Open your terminal in the project's root directory and run the following command:

streamlit run app.py

☁️ Deployment to Streamlit Community Cloud
1. Prerequisites
GitHub Account: You need a GitHub account.

Push Project to GitHub: Create a new repository on GitHub and push all your project files (app.py, utils.py, requirements.txt, etc.) to it. Do not push your secrets.toml file.

2. Deployment Steps
Sign up/in: Go to Streamlit Community Cloud and sign up or log in with your GitHub account.

New App: Click the "New app" button from your workspace.

Configure Deployment:

Repository: Select the GitHub repository where you pushed your project.

Branch: Select the main branch.

Main file path: Ensure this is set to app.py.

App URL: Give your app a custom URL.

Add Secrets: Before you deploy, you must add your API keys to the Streamlit Cloud environment.

Click on the "Advanced settings..." dropdown.

In the "Secrets" section, copy and paste the entire content of your local secrets.toml file.

Deploy: Click the "Deploy!" button. Streamlit will build and launch your application.

Your research agent will now be live and accessible to anyone with the URL.