# Call Transcript Analyzer (Flask + Groq)

## What
Simple web app that summarizes customer call transcripts and extracts sentiment using the Groq API. Results are saved to call_analysis.csv.

## Run locally (Windows PowerShell)
1. Create & activate venv:
   python -m venv venv
   venv\Scripts\Activate.ps1

2. Install:
   pip install -r requirements.txt

3. Set API key (current session):
   $env:GROQ_API_KEY="your_key_here"

4. Run:
   python app.py

5. Open:
   http://127.0.0.1:5000/

