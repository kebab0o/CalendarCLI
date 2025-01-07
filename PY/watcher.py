import time
import json
from datetime import datetime, timedelta
import notification_utils as nu

WATCH_PATH = r"C:\Windows\System32\data"
EVENTS_FILE = WATCH_PATH + r"\events.json"

def load_events():
    try:
        with open(EVENTS_FILE, "r") as file:
            data = json.load(file)
            events = data.get("events", [])
            event_list = []
            for event in events:
                event_list.append({
                    "title": event["Title"],
                    "description": event["Description"],
                    "notification": datetime.strptime(event["Notification"], "%Y-%m-%d-%H:%M"),
                    "time": event["Time"]
                })
            return event_list
    except FileNotFoundError:
        print("File not found:", EVENTS_FILE)
        return []
    except Exception as e:
        print("Error loading events:", e)
        return []

def watch():
    print("Watcher service started...")
    while True:
        try:
            events = load_events()
            now = datetime.now()
            for event in events:
                if now >= event["notification"] and now < event["notification"] + timedelta(minutes=5):
                    nu.display_notification(event["title"], event["time"], event["description"])
            time.sleep(60)
        except Exception as e:
            print("Error in watcher loop:", e)

if __name__ == "__main__":
    watch()
