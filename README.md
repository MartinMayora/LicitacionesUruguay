# Licitaciones Daily Automation

A Python-based automation tool that delivers **daily emails with public tenders (licitaciones) from Uruguay**.  
It uses Google's Gemini API to process and filter tender data, sending you only the categories that matter to you.  

You can easily customize the categories by adjusting the **prompt** used in the script.

---

## Features
- **Automated daily execution** (via cron or task scheduler)  
- **Email notifications** with fresh tender opportunities  
- **Category filtering** based on a customizable Gemini prompt  
- **Catch-up mode** if the system was offline  
- **State tracking** to avoid duplicates  
- **Logging** for monitoring and debugging  

---

## Setup

### 1. Requirements
- Python **3.x**
- A scheduling service (Linux cron, Windows Task Scheduler, etc.)

### 2. Install Dependencies
```bash
pip install python-dotenv google-generativeai
```

### 3. Configure Environment
Create a `.env` file in the project root with the following variables:

```env
SENDER_EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password
GEMINI_API_KEY=your_gemini_api_key
```

- **SENDER_EMAIL** → your Gmail address (the sender)  
- **APP_PASSWORD** → [Gmail App Password](https://support.google.com/accounts/answer/185833) (requires 2FA enabled)  
- **GEMINI_API_KEY** → create one at [Google AI Studio](https://aistudio.google.com/)  

---

## Usage

1. **Schedule the script**  
   - On Linux: use `cron`  
   - On Windows: use **Task Scheduler**  

   Example cron job (runs once per day at 9 AM):
   ```bash
   0 9 * * * /usr/bin/python /path/to/licitaciones-automation/cron_licitaciones.py >> /path/to/licitaciones-automation/cron_licitaciones.log 2>&1
   ```

2. **Customize the categories**  
   - Open `cron_licitaciones.py`  
   - Modify the **Gemini prompt** to focus on the categories you care about (e.g., `"Filter tenders about software, IT services, and consulting"`)  

3. **Receive daily emails** with the filtered tenders.  

---

## 📂 Project Structure
```
licitaciones-automation/
├── cron_licitaciones.py     # Main script
├── script_state.json        # Tracks last processed day (auto-generated)
├── .env                     # Environment variables (user-provided)
└── cron_licitaciones.log    # Log file (auto-generated)
```

---

## How It Works
1. **Scheduling** → script runs daily (or hourly if configured)  
2. **State Tracking** → remembers the last processed day to avoid duplicates  
3. **Catch-up Logic** → if the system was off, it processes missed days  
4. **Email Notifications** → sends a daily summary of tenders matching your categories  
5. **Logging** → activity is stored in `cron_licitaciones.log`  

---

## Monitoring

Check logs:
```bash
tail -f cron_licitaciones.log
```

Check cron service status (Linux):
```bash
systemctl status cronie
```

View cron execution logs:
```bash
journalctl -u cronie -f
```

---

## Manual Execution
You can also run the script manually:
```bash
python cron_licitaciones.py
```

---

## Troubleshooting

### Cron job not running
- Verify cron is active:
  ```bash
  systemctl status cronie
  ```
- List configured jobs:
  ```bash
  crontab -l
  ```

### Python path issues
- Check Python location:
  ```bash
  which python
  ```
- Update the cron job with the correct path if needed.

### Email sending failures
- Confirm Gmail App Password is valid.  
- Ensure `.env` has correct credentials.  

### API key issues
- Check if your Gemini API key is valid and has quota.  
- Ensure you have internet access.  

---

## Security Notes
- Do **not** commit `.env` to version control.  
- Regularly rotate your Gmail App Password and Gemini API key.  
- Restrict API key permissions whenever possible.  

---

## Notes
- The categories of tenders are **fully customizable** via the Gemini prompt.  
- The project currently targets **Uruguayan public tenders**, but it can be adapted to other sources.  
- Best suited for always-on systems (e.g., server, VPS, Raspberry Pi, or cloud VM).  

---
