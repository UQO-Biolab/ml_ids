import json
from scapy.all import *
from binascii import unhexlify

def valid_port(p): return isinstance(p, int) and 0 <= p <= 65535

with open("honeytrap_coma.json", "r") as f_json, PcapWriter("honeytrap_output.pcap", append=False, sync=True) as pcap:
    data = json.load(f_json)
    for i, attack in enumerate(data["attacks"]):
        conn = attack.get("attack_connection", {})
        proto = conn.get("protocol", "").lower()
        src_ip = conn.get("remote_ip")
        dst_ip = conn.get("local_ip")
        src_port = conn.get("remote_port", -1)
        dst_port = conn.get("local_port", -1)

        if not (valid_port(src_port) and valid_port(dst_port)):
            print(f"[SKIPPED] Line {i} invalid ports: src={src_port}, dst={dst_port}")
            continue

        payload = b""
        try:
            payload_hex = conn.get("payload", {}).get("data_hex", "")
            if payload_hex:
                payload = unhexlify(payload_hex)
        except Exception as e:
            print(f"[PAYLOAD ERROR] Line {i}: {e}")
            continue

        try:
            if proto == "tcp":
                pkt = IP(src=src_ip, dst=dst_ip)/TCP(sport=src_port, dport=dst_port)/payload
            elif proto == "udp":
                pkt = IP(src=src_ip, dst=dst_ip)/UDP(sport=src_port, dport=dst_port)/payload
            else:
                continue
            pcap.write(pkt)
        except Exception as e:
            print(f"[PACKET CREATION ERROR] Line {i}: {e}")
