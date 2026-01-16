import socket

def parse_http_path(request: str) -> str:
    first_line: str = request.splitlines()[0]
    _, path, _ = first_line.split()
    return path

def http_response(body: str, status: str = "200 OK") -> bytes:
    response: str = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        "\r\n"
        f"{body}"
    )
    return response.encode("utf-8")

def handle_client(client_socket: socket.socket) -> None:
    request_bytes: bytes = client_socket.recv(1024)
    request: str = request_bytes.decode("utf-8", errors="ignore")
    path: str = parse_http_path(request)
    
    if path == "/":
        body: str = "<h1>Hello, world!</h1>"
        response: bytes = http_response(body)
    elif path == "/about":
        body = "<h1>About</h1><p>Tiny blocking server.</p>"
        response = http_response(body)
    else:
        body = "<h1>404 Not Found</h1>"
        response = http_response(body, status="404 Not Found")
    
    client_socket.sendall(response)
    client_socket.close()

def main() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 8000))
    server_socket.listen(5)
    
    # Set a timeout so accept() won't block forever
    server_socket.settimeout(1.0)  # 1 second
    
    print("Serving on http://127.0.0.1:8000")
    print("Press Ctrl+C to stop")
    print("WARNING: This server handles ONE request at a time!")
    
    try:
        while True:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")
                handle_client(client_socket)
            except socket.timeout:
                # Timeout allows us to check for KeyboardInterrupt regularly
                continue
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
