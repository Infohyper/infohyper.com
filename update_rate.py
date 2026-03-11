import os
import json
import datetime
from google import genai
import traceback

# Setup the new Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def get_live_rates():
    prompt = (
        "Search for the current Roblox DevEx rate and the current Retail rate for 1 Robux in USD. "
        "Return ONLY a raw JSON object: {'devex': 0.0038, 'retail': 0.0125}."
    )
    
    # Using the new model from your screenshot
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=prompt
    )
    
    # Clean the response
    raw_text = response.text.strip().replace("```json", "").replace("```", "").strip().replace("'", '"')
    return json.loads(raw_text)

# --- MAIN EXECUTION ---
folder_path = "data"
os.makedirs(folder_path, exist_ok=True)

try:
    rates = get_live_rates()
    rates["updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(f"{folder_path}/rubux-rate.json", 'w') as f:
        json.dump(rates, f, indent=4)
    
    if os.path.exists(f"{folder_path}/error.txt"):
        os.remove(f"{folder_path}/error.txt")
        
    print("Success: rates updated using Gemini 3 Flash.")

except Exception as e:
    error_message = f"Error Date: {datetime.datetime.now()}\nMessage: {str(e)}\n{traceback.format_exc()}"
    with open(f"{folder_path}/error.txt", 'w') as f:
        f.write(error_message)
    print("FAILED: Check error.txt")
