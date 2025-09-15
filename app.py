from flask import Flask, request, render_template_string
import os
import pandas as pd
from groq import Groq
import json

app = Flask(__name__)

# --- Groq Client ---
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- CSV file ---
CSV_FILE = "call_analysis.csv"

# --- Simple HTML form ---
HTML = """
<h2>Call Transcript Analyzer</h2>
<form method="post" action="/analyze">
  <textarea name="transcript" rows="6" cols="60" placeholder="Paste transcript here..."></textarea><br>
  <input type="submit" value="Analyze">
</form>
{% if result %}
<hr>
<h3>Result</h3>
<b>Transcript:</b> {{ result.transcript }}<br>
<b>Summary:</b> {{ result.summary }}<br>
<b>Sentiment:</b> {{ result.sentiment }}
{% endif %}
"""

# --- Routes ---
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML)

@app.route("/analyze", methods=["POST"])
def analyze():
    transcript = request.form.get("transcript")
    if not transcript:
        return "Please enter a transcript!", 400

    try:
        #--- Groq API call ---
        "You are an assistant. Summarize in 2–3 sentences and give sentiment (Positive/Neutral/Negative). Return JSON only."
        system_msg = "You are an assistant. Summarize in 2–3 sentences and give sentiment (Positive/Neutral/Negative). Return JSON only."
        user_msg = f"Transcript:\n{transcript}"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Replace with the new model ID
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ]
        )

        content = response.choices[0].message.content
        data = json.loads(content)  # Expect JSON like {"summary": "...", "sentiment": "..."}

        summary = data.get("summary", "")
        sentiment = data.get("sentiment", "")

        # --- Save to CSV ---
        df = pd.DataFrame([{
            "Transcript": transcript,
            "Summary": summary,
            "Sentiment": sentiment
        }])
        if not os.path.exists(CSV_FILE):
            df.to_csv(CSV_FILE, index=False)
        else:
            df.to_csv(CSV_FILE, mode="a", header=False, index=False)

        # --- Show result on page ---
        return render_template_string(HTML, result={"transcript": transcript, "summary": summary, "sentiment": sentiment})

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
