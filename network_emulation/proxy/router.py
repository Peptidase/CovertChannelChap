import socket
import threading

INTERNAL_IP = "0.0.0.0"
INTERNAL_PORT = 8080

def handle_client(client_socket):
    # Read the first packet to determine the destination
    data = client_socket.recv(65535)
    if not data:
        client_socket.close()
        return

    # For simplicity, forward everything to the internet as-is
    # Here we hardcode Google's DNS to prove internet access
    remote_host = "8.8.8.8"
    remote_port = 80

    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        remote_socket.connect((remote_host, remote_port))
        remote_socket.send(data)
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        client_socket.close()
        return

    def forward(src, dst):
        while True:
            try:
                chunk = src.recv(4096)
                if not chunk:
                    break
                dst.send(chunk)
            except:
                break
        src.close()
        dst.close()

    threading.Thread(target=forward, args=(client_socket, remote_socket)).start()
    threading.Thread(target=forward, args=(remote_socket, client_socket)).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((INTERNAL_IP, INTERNAL_PORT))
    server.listen(50)
    print(f"[+] Software router listening on {INTERNAL_PORT}")

    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,)).start()

if __name__ == "__main__":
    main()
