import socketserver
import requests
import http.server





# Detect the http google search request and then edit and resend the webpage






PORT = 8080
TARGET_HOST = "www.google.com"  # Change to the website you want to intercept

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_REQUEST(self):
        # Build the target URL
        url = f"http://{TARGET_HOST}{self.path}"

        # Collect headers from the client
        headers = {key: value for key, value in self.headers.items()}

        # Read the request body if present
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Forward the request to the target server
        resp = requests.request(
            method=self.command,
            url=url,
            headers=headers,
            data=body,
            allow_redirects=False
        )
        content = resp.content

        # Optionally edit the HTML body
        if "text/html" in resp.headers.get("Content-Type", ""):
            content = content.replace(b"</body>", b"<!-- Intercepted -->\n</body>")

        # Send response status and headers
        self.send_response(resp.status_code)
        for key, value in resp.headers.items():
            if key.lower() in ["content-encoding", "content-length"]:
                continue
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    # Map all HTTP methods to do_REQUEST
    def do_GET(self): self.do_REQUEST()
    def do_POST(self): self.do_REQUEST()
    def do_PUT(self): self.do_REQUEST()
    def do_DELETE(self): self.do_REQUEST()
    def do_HEAD(self): self.do_REQUEST()
    def do_OPTIONS(self): self.do_REQUEST()
    def do_PATCH(self): self.do_REQUEST()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ProxyHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()