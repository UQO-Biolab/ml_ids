import json

# Valid port range
MIN_PORT = 0
MAX_PORT = 65535

# Load the JSON file
with open("honeytrap_coma_1500.json", "r") as f:
    data = json.load(f)

# Port validation
for i, attack in enumerate(data.get("attacks", [])):
    conn = attack.get("attack_connection", {})

    remote_port = conn.get("remote_port", -1)
    local_port = conn.get("local_port", -1)

    if not (MIN_PORT <= remote_port <= MAX_PORT) or not (MIN_PORT <= local_port <= MAX_PORT):
        print(f"Line {i}: remote_port={remote_port}, local_port={local_port}")
