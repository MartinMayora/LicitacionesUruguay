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
            return json.load(f)
    except FileNotFoundError:
        return {"last_processed_day": None}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def main():
    state = load_state()
    today = date.today()
    
    if state["last_processed_day"]:
        last_day = date.fromisoformat(state["last_processed_day"])
        start_day = last_day + timedelta(days=1)
    else:
        start_day = today  

    if start_day > today:
        print("No days to process")
        return
    
    current_day = start_day
    while current_day <= today:
        print(f"Processing: {current_day}")
        
        run_daily_job(current_day)
        
        state["last_processed_day"] = current_day.isoformat()
        save_state(state)
        
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