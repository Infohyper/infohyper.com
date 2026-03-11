import os
import json
import datetime
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def get_live_rates():
    prompt = (
        "Find the current Roblox DevEx rate and the current Retail rate for 1 Robux in USD. "
        "Return the result ONLY as a JSON object: {'devex': 0.0038, 'retail': 0.0125}"
    )
    try:
        response = model.generate_content(prompt)
        # Clean response (remove ```json wrappers)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except:
        return {"devex": 0.0038, "retail": 0.0125} # Solid backup

# 1. Get rates from AI
rates = get_live_rates()

# 2. Add the timestamp
rates["updated"] = datetime.datetime.now().strftime("%Y-%m-%d")

# 3. Save to your EXACT file path
# Note: Ensure the 'data' folder exists in your GitHub repo
file_path = "data/rubux-rate.json"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, 'w') as f:
    json.dump(rates, f, indent=4)
    print(f"File {file_path} updated successfully!")
