import os
import json
import datetime
import google.generativeai as genai
import traceback

# Setup
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def get_live_rates():
    prompt = (
        "Search for the current Roblox DevEx rate and the current Retail rate for 1 Robux in USD. "
        "Return ONLY a raw JSON object: {'devex': 0.0038, 'retail': 0.0125}."
    )
    
    # We do NOT use try/except inside the function anymore
    # because we want to catch the error in the main part of the script.
    response = model.generate_content(prompt)
    raw_text = response.text.strip().replace("```json", "").replace("```", "").strip().replace("'", '"')
    return json.loads(raw_text)

# --- MAIN EXECUTION ---
folder_path = "data"
os.makedirs(folder_path, exist_ok=True)

try:
    # Try to get the data
    rates = get_live_rates()
    rates["updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # If successful, save the JSON
    with open(f"{folder_path}/rubux-rate.json", 'w') as f:
        json.dump(rates, f, indent=4)
    
    # Also, remove error.txt if it exists from a previous failed run
    if os.path.exists(f"{folder_path}/error.txt"):
        os.remove(f"{folder_path}/error.txt")
        
    print("Success: rates updated.")

except Exception as e:
    # If ANY error happens, write it to error.txt
    error_message = f"Error Date: {datetime.datetime.now()}\n"
    error_message += f"Message: {str(e)}\n"
    error_message += f"Traceback:\n{traceback.format_exc()}"
    
    with open(f"{folder_path}/error.txt", 'w') as f:
        f.write(error_message)
        
    print("FAILED: Error written to error.txt")
