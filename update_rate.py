import os
import json
import datetime
from google import genai
import traceback

# Setup
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_live_rates():
    prompt = "Search for current Roblox DevEx and Retail rates. Return ONLY raw JSON: {'devex': 0.0038, 'retail': 0.0125}"
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    text = response.text.strip().replace("```json", "").replace("```", "").strip().replace("'", '"')
    return json.loads(text)

# --- EXECUTION ---
# Force directory creation
os.makedirs("data", exist_ok=True)

try:
    rates = get_live_rates()
    rates["updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("data/rubux-rate.json", "w") as f:
        json.dump(rates, f, indent=4)
    
    if os.path.exists("data/error.txt"):
        os.remove("data/error.txt")
    print("SUCCESS: JSON file written to data/rubux-rate.json")

except Exception as e:
    with open("data/error.txt", "w") as f:
        f.write(f"Error: {str(e)}\n{traceback.format_exc()}")
    print("FAILURE: Error written to data/error.txt")
