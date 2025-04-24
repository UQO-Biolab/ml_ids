import json
import csv
from collections import defaultdict
from datetime import datetime

json_path = "fusion_cowrie_filtered.json"
csv_path = "cowrie_sessions.csv"

def is_business_hours(start_time):
    # Assume start_time is an ISO 8601 string (e.g. '2025-04-14T14:30:00')
    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ")  # Convert to datetime object
    hour = start_time.hour - 5  # Adjust for timezone if needed
    return 8 <= hour < 18  # Between 8 AM and 6 PM

# Group events by session
sessions = defaultdict(list)

with open(json_path, "r") as file:
    for line in file:
        try:
            event = json.loads(line)
            session_id = event.get("session")
            if session_id:
                sessions[session_id].append(event)
        except json.JSONDecodeError:
            print("Corrupted line", line)

# Prepare the dataset
dataset = []

for session_id, events in sessions.items():
    session_data = {
        "session_id": session_id,
        "start_time": None,
        "end_time": None,
        "duration": None,
        "src_ip": None,
        "src_port": None,
        "dst_port": None,
        "protocol": None,
        "total_connexion": 0,
        "login_failed": 0,
        "login_success": 0,
        "avg_time_between_failed": 0,
        "is_business_hours": True,
        #"username": None,
        #"password": None,
        #"commands": [],
        #"downloads": [],
        #"tty_output": [],
        #"client": None,
        #"sensor": None,
    }

    failed_timestamps = []

    for event in events:
        eid = event.get("eventid")

        if eid == "cowrie.session.connect":
            session_data["start_time"] = event.get("timestamp")
            session_data["src_ip"] = event.get("src_ip")
            session_data["src_port"] = event.get("src_port")
            session_data["dst_port"] = event.get("dst_port")
            session_data["protocol"] = event.get("protocol")
            session_data["sensor"] = event.get("sensor", None)
            session_data["total_connexion"] += 1
            session_data["is_business_hours"] = is_business_hours(event.get("timestamp"))

        elif eid == "cowrie.session.closed":
            session_data["end_time"] = event.get("timestamp")
            session_data["duration"] = event.get("duration")

        elif eid == "cowrie.login.failed":
            session_data["login_failed"] += 1
            session_data["total_connexion"] += 1
            failed_timestamps.append(event.get("timestamp"))

        elif eid == "cowrie.login.success":
            session_data["total_connexion"] += 1
            session_data["login_success"] += 1

        #elif eid == "cowrie.command.input":
            #session_data["commands"].append(event.get("input"))

        #elif eid == "cowrie.session.file_download":
            #f = event.get("outfile") or event.get("shasum") or event.get("url") or "unknown"
            #session_data["downloads"].append(f)

        #elif eid == "cowrie.log.closed":
            #if event.get("ttylog"):
                #session_data["tty_output"].append(event.get("ttylog"))

        #elif eid == "cowrie.client.version":
            #session_data["client"] = event.get("version")

    # Compute average time between failed logins
    if len(failed_timestamps) >= 2:
        try:
            times = [datetime.fromisoformat(ts.replace("Z", "+00:00")) for ts in failed_timestamps]
            times.sort()
            diffs = [(t2 - t1).total_seconds() for t1, t2 in zip(times, times[1:])]
            avg_diff = sum(diffs) / len(diffs)
            session_data["avg_time_between_failed"] = round(avg_diff, 3)
        except Exception as e:
            print(f"Timestamp parsing error for session {session_id}: {e}")

    # Final cleanup
    dataset.append({
        "session_id": session_data["session_id"],
        "start_time": session_data["start_time"],
        "end_time": session_data["end_time"],
        "duration": session_data["duration"],
        "src_ip": session_data["src_ip"],
        "src_port": session_data["src_port"],
        "dst_port": session_data["dst_port"],
        "protocol": session_data["protocol"],
        "total_connexion": session_data["total_connexion"],
        "login_success": session_data["login_success"],
        "login_failed": session_data["login_failed"],
        "avg_time_between_failed": session_data["avg_time_between_failed"],
        "is_business_hours": session_data["is_business_hours"],
        "label": 0
        #"username": session_data["username"],
        #"password": session_data["password"],
        #"commands": "; ".join(session_data["commands"]),
        #"downloads": "; ".join(session_data["downloads"]),
        #"tty_output": "; ".join(session_data["tty_output"]),
        #"client": session_data["client"],
        #"sensor": session_data["sensor"],
    })

# Write CSV
with open(csv_path, "w", newline='', encoding="utf-8") as f:
    fieldnames = list(dataset[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(dataset)

print(f"{len(dataset)} sessions written to {csv_path}")
