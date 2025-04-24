import json
from datetime import datetime, timedelta, timezone
from tqdm import tqdm
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
EVE_FILE = 'eve.json'
HONEYPOT_FILE = 'honeytrap.json'
OUTPUT_FILE = 'ids.json'
TIME_TOLERANCE_SECONDS = 500
NUM_THREADS = 4

def parse_timestamp(ts):
    try:
        if ts.endswith('Z'):
            try:
                # With microseconds
                return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            except ValueError:
                # Without microseconds
                return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        else:
            # Suricata format: +0000
            return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError as e:
        print(f"Timestamp parsing error: {ts} → {e}")
        return None

def extract_ips(event):
    ips = set()
    for field in ['src_ip', 'dest_ip', 'src', 'dst', 'host']:
        if field in event:
            ips.add(event[field])
    return ips

def load_events(filepath):
    events = []
    with open(filepath, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                timestamp = data.get('timestamp') or data.get('@timestamp') or data.get('time') or data.get('date')
                if timestamp:
                    parsed_ts = parse_timestamp(timestamp)
                    if parsed_ts:
                        data['_parsed_ts'] = parsed_ts
                        data['_ips'] = extract_ips(data)
                        events.append(data)
            except json.JSONDecodeError:
                continue
    return events

def index_events_by_ip(events):
    ip_index = defaultdict(list)
    for event in events:
        for ip in event['_ips']:
            ip_index[ip].append(event)
    return ip_index

def find_matches_batch(eve_batch, cowrie_index):
    local_matches = []
    for eve in eve_batch:
        checked = set()
        for ip in eve['_ips']:
            for cowrie in cowrie_index.get(ip, []):
                if id(cowrie) in checked:
                    continue
                checked.add(id(cowrie))
                time_diff = abs((eve['_parsed_ts'] - cowrie['_parsed_ts']).total_seconds())
                if time_diff <= TIME_TOLERANCE_SECONDS:
                    local_matches.append({
                        'eve_event': eve,
                        'cowrie_event': cowrie
                    })
    return local_matches

def split_batches(data, num_batches):
    batch_size = max(1, len(data) // num_batches)
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

def main():
    print("Loading Suricata events...")
    eve_events = load_events(EVE_FILE)
    print(f"{len(eve_events)} events loaded")

    print("Loading Cowrie events...")
    cowrie_events = load_events(HONEYPOT_FILE)
    print(f"{len(cowrie_events)} events loaded")

    print("Indexing Cowrie events...")
    cowrie_index = index_events_by_ip(cowrie_events)

    print(f"Finding matches using {NUM_THREADS} threads...")
    eve_batches = split_batches(eve_events, NUM_THREADS)
    all_matches = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = [executor.submit(find_matches_batch, batch, cowrie_index) for batch in eve_batches]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Parallel processing"):
            all_matches.extend(future.result())

    print(f"Writing {len(all_matches)} matches...")
    with open(OUTPUT_FILE, 'w') as out:
        for match in all_matches:
            json.dump(match, out)
            out.write('\n')

    print(f"\n✅ Done: {len(all_matches)} matches written to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
