import pyshark
import socket
import struct
import time
from collections import defaultdict
import pandas as pd
import joblib
from datetime import timedelta
import collections

# Bruteforce detection parameters
bruteforce_attempts = collections.defaultdict(list)
BRUTEFORCE_WINDOW_SECONDS = 60
BRUTEFORCE_THRESHOLD = 5

# Tracking dictionnary
ip_conn_counter = defaultdict(int)
failed_logins = defaultdict(list)
sessions = defaultdict(lambda: {
    'total_connexion': 0,
    'login_success': 0,
    'login_failed': 0,
    'avg_time_between_failed': 0.0,
    'login_timestamps': [],
    'is_business_hours': 0
})
active_connections = {}

def ip_to_int(ip):
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except:
        return 0

def is_business_hours(timestamp):
    return 9 <= timestamp.hour < 18

def detect_bruteforce(ip_src, timestamp, service="SSH"):
    attempts = bruteforce_attempts[(ip_src, service)]
    now = timestamp

    attempts.append(now)

    window_start = now - timedelta(seconds=BRUTEFORCE_WINDOW_SECONDS)
    bruteforce_attempts[(ip_src, service)] = [t for t in attempts if t > window_start]

    if len(bruteforce_attempts[(ip_src, service)]) >= BRUTEFORCE_THRESHOLD:
        print(f"🚨 [Bruteforce {service}] IP : {ip_src} ({len(attempts)} temptations in {BRUTEFORCE_WINDOW_SECONDS}s)")
    

def extract_features(packet):
    try:
        timestamp = packet.sniff_time
        ip_src = packet.ip.src
        ip_dst = packet.ip.dst
        src_port = int(getattr(packet.tcp, 'srcport', 0))
        dst_port = int(getattr(packet.tcp, 'dstport', 0))

        flags_raw = packet.tcp.flags
        flag_value = int(flags_raw, 16)

        flags = {
            'FIN': bool(flag_value & 0x01),
            'SYN': bool(flag_value & 0x02),
            'RST': bool(flag_value & 0x04),
            'PSH': bool(flag_value & 0x08),
            'ACK': bool(flag_value & 0x10),
            'URG': bool(flag_value & 0x20),}

        #print(f"Packet {packet.ip.src}:{packet.tcp.srcport} → {packet.ip.dst}:{packet.tcp.dstport}")
        flag_final_value = "-".join([k for k, v in flags.items() if v])
        #print("TCP Flags actifs :", ", ".join([f for f, v in flags.items() if v]))

        # Only SSH/Telnet
        if dst_port not in [22, 23]:
            return None
        
        if dst_port == 22 and flag_final_value == 'SYN':
            detect_bruteforce(ip_src, timestamp, service="SSH")
            active_connections[(ip_src, ip_dst, src_port, dst_port)] = float(packet.sniff_timestamp)

        elif dst_port == 23 and flag_final_value == 'SYN':
            detect_bruteforce(ip_src, timestamp, service="Telnet")
            active_connections[(ip_src, ip_dst, src_port, dst_port)] = float(packet.sniff_timestamp)

        # End of connexion (RST or FIN)
        if flag_final_value in ['FIN', 'RST', 'FIN-ACK']:
            conn_id = (ip_src, ip_dst, src_port, dst_port)
            start_time = active_connections.pop(conn_id, None)

            if not start_time:
                reversed_conn_id = (ip_dst, ip_src, dst_port, src_port)
                start_time = active_connections.pop(reversed_conn_id, None)

            #print("Start time:", start_time)
            if dst_port == 22:
                print(f"End of session SSH {ip_src} -> {ip_dst}")
            elif dst_port == 23:
                print(f"End of session Telnet {ip_src} -> {ip_dst}")

            if start_time:
                end_time = float(packet.sniff_timestamp)
                duration = end_time - start_time
                #print("Duration:", duration)

                login_success = 0
                login_failed = 0

                # Update tracking
                ip_conn_counter[ip_src] += 1
                if login_failed:
                    failed_logins[ip_src].append(time.time())

                timestamps = failed_logins[ip_src]
                if len(timestamps) >= 2:
                    diffs = [t - s for s, t in zip(timestamps[:-1], timestamps[1:])]
                    avg_fail_time = sum(diffs) / len(diffs)
                else:
                    avg_fail_time = 0.0

                session = sessions[ip_src]
                session['total_connexion'] = ip_conn_counter[ip_src]
                session['login_success'] += 1
                session['login_failed'] += login_failed
                session['avg_time_between_failed'] = avg_fail_time
                session['is_business_hours'] = is_business_hours(timestamp)

                return {
                    'duration': duration,
                    'src_ip_int': ip_to_int(ip_src),
                    'src_port': src_port,
                    'dst_port': dst_port,
                    'protocol': 0 if dst_port == 22 else 1,
                    'total_connexion': session['total_connexion'],
                    'login_success': session['login_success'],
                    'login_failed': session['login_failed'],
                    'avg_time_between_failed': session['avg_time_between_failed'],
                    'is_business_hours': session['is_business_hours']
                }
    except AttributeError:
        return None

# Sniffing
# Put the correct interface for your case
capture = pyshark.LiveCapture(interface='ens160', display_filter='tcp.port == 22 or tcp.port == 23')
print("Sniffing... Ctrl+C to stop.")
try:
    for packet in capture.sniff_continuously():
        feats = extract_features(packet)
        if feats:
            df = pd.DataFrame([feats])
            print(df)
            model = joblib.load('model_cowrie.pkl')
            features = [ 'duration', 'src_ip_int', 'src_port', 'dst_port', 'protocol', 'total_connexion', 'login_success', 'login_failed', 'avg_time_between_failed', 'is_business_hours']
            x = pd.DataFrame(df, columns=features)
            result = model.predict(x)
            ("Raw result :", result)
            if result[0] == 1:
                print("🚨 Alert")
            else:
                print("✅ Normal")
except KeyboardInterrupt:
    print("\n🛑 Stop by user.")
    capture.close()


