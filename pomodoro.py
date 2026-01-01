import time
from datetime import datetime
import json
import matplotlib.pyplot as plt

FOCUS_MINUTES = 25
BREAK_MINUTES = 5
SESSIONS = 4

LOG_FILE = "focus_log.json"
DISTRACTIONS = ["youtube.com", "tiktok.com", "instagram.com"]

def block_sites():
    print("🚫 Blocking distractions...")
    for site in DISTRACTIONS:
        print(f"   blocked: {site}")

def unblock_sites():
    print("✅ Unblocking sites...")

def save_log(minutes):
    data = []
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        pass

    data.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "focus_minutes": minutes
    })

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def show_stats():
    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    dates = [d["date"] for d in data]
    minutes = [d["focus_minutes"] for d in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, minutes, marker="o")
    plt.title("Focus Time Statistics")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ===== RUN =====
total_focus = 0

for session in range(SESSIONS):
    print(f"\n🔥 Focus session {session + 1}")
    block_sites()

    for m in range(FOCUS_MINUTES):
        print(f"⏳ Focus... {m + 1} min")
        time.sleep(1)  # ускорено для видео

    unblock_sites()
    total_focus += FOCUS_MINUTES

    print("☕ Break time")
    time.sleep(2)

save_log(total_focus)
show_stats()
