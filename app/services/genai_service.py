import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()  

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_diabetes_resources():
    
    prompt = """
    Suggest 3 helpful and trustworthy articles or resources for a person
    recently diagnosed with diabetes. Include only verified sources like WHO,
    Mayo Clinic, WebMD, or NIH. Provide short titles and links.
    Return as a simple JSON list of objects like:
    [
      {"title": "Managing Type 2 Diabetes", "url": "..."},
      {"title": "Healthy Eating for Diabetes", "url": "..."}
    ]
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()  # remove leading/trailing whitespace
        # Remove ```json fences if they exist
        if text.startswith("```json"):
            text = text[len("```json"):].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        # Parse into Python list
        return json.loads(text)
    except Exception as e:
        print("Error generating AI resources:", e)
        return []
