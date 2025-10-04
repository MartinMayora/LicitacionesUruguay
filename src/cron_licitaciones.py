from datetime import date, timedelta
import json
import sys
import os

sys.path.append(os.path.dirname(__file__))
from main_licitaciones import get_licitaciones_send_email

STATE_FILE = "script_state.json"

def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            content = json.load(f)
            print(f"Loaded state content: {content}")
            return content
    except FileNotFoundError:
        print("State file not found, starting fresh")
        return {"last_processed_day": None}
    except json.JSONDecodeError as e:
        print(f"Error parsing state file: {e}")
        return {"last_processed_day": None}

def save_state(state):
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)  # Add indent for readability
        print(f"State saved successfully to {STATE_FILE}")
        # Verify the file was written
        if os.path.exists(STATE_FILE):
            print("State file exists after save")
            with open(STATE_FILE, 'r') as f:
                saved_content = json.load(f)
                print(f"Verified saved content: {saved_content}")
    except Exception as e:
        print(f"Error saving state: {e}")
def main():
    state = load_state()
    today = date.today()
    print(f"Loaded state: {state}")
    print(f"Today: {today}")
    
    if state["last_processed_day"]:
        last_day = date.fromisoformat(state["last_processed_day"])
        start_day = last_day + timedelta(days=1)
        print(f"Last processed day: {last_day}, Start day: {start_day}")
    else:
        start_day = today
        print(f"No previous state, starting from: {start_day}")

    if start_day > today:
        print("No days to process")
        return
    
    current_day = start_day
    print(f"Processing from {current_day} to {today}")
    
    while current_day <= today:
        print(f"Processing: {current_day}")
        try:
            run_daily_job(current_day)
            
            state["last_processed_day"] = current_day.isoformat()
            save_state(state)
            print(f"Successfully saved state for: {current_day}")
            
        except Exception as e:
            print(f"Error processing {current_day}: {e}")
            # Don't proceed to next day if current day failed
            return
        
        current_day += timedelta(days=1)
    
    print("All days processed up to", today)

def get_previous_day_string(target_date):
    previous_day = target_date - timedelta(days=1)
    return previous_day.strftime("%d-%m-%Y")

def run_daily_job(day):
    previous_day = get_previous_day_string(day)
    get_licitaciones_send_email(previous_day)
    
if __name__ == "__main__":
    main()