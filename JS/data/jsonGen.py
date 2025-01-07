import json
from datetime import datetime, timedelta
import random

# Generate a JSON file with 10,000 events
def generate_events(file_name):
    events = []
    start_date = datetime(2024, 1, 1)

    for i in range(10000):
        event_date = start_date + timedelta(days=random.randint(0, 364))
        formatted_date = event_date.strftime("%Y-%m-%d")
        notification_time = (event_date - timedelta(hours=2)).strftime("%Y-%m-%d:%H:%M")

        event = {
            "title": f"Event {i+1}",
            "date": formatted_date,
            "description": "Description of the event.",
            "time": "09:00",
            "notification": notification_time
        }
        events.append(event)

    data = {"events": events}

    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)

# Specify the output file name
output_file = "events.json"
generate_events(output_file)
print(f"Generated {output_file} with 10,000 events.")