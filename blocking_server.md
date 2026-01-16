# Blocking Python HTTP Server

This is a **minimal, fully synchronous HTTP server** written in Python. It is intended as a **learning tool** to help beginners understand how web servers work at the most basic level.  

> ⚠️ This server is blocking — it handles **one request at a time** and is not suitable for production.

> ⚠️ The server now uses a short socket timeout so that Ctrl+C can stop the server immediately, even if no clients are connected.

---

## How It Works

1. The server creates a TCP socket and listens on `127.0.0.1:8000`.
2. It sets a 1-second timeout on the socket to prevent accept() from blocking indefinitely.
3. When a client connects (e.g., a web browser), it **receives the HTTP request**.
4. It parses the request to find the requested path.
5. Depending on the path:
   - `/` → returns a "Hello, world!" HTML page
   - `/about` → returns a simple "About" page
   - anything else → returns a "404 Not Found" page
6. The server sends the HTTP response back to the client and closes the connection.
7. If no client connects within the timeout, the server loops again, allowing keyboard interrupts (Ctrl+C) to be detected immediately.

---

## Features

- Minimal HTTP parsing (only handles simple GET requests)
- Routes for `/` and `/about`
- 404 page for unknown paths
- Synchronous/blocking — handles **one connection at a time**
- Socket timeout enables immediate Ctrl+C handling
- Minimal HTML responses

---

## How to Run

1. Make sure you have **Python 3.8+** installed.
2. Save the server code as `blocking_server.py`.
3. Run the server:


        python blocking_server.py


Open your browser and visit:

http://127.0.0.1:8000/
 → Hello, world!

http://127.0.0.1:8000/about
 → About page

- Any other path → 404 page
- Stop the server with Ctrl+C.

## Code Overview

Parsing Requests
```python
      def parse_http_path(request: str) -> str:
          first_line = request.splitlines()[0]
          _, path, _ = first_line.split()
          return path
```
Extracts the path from a simple HTTP GET request.

## Sending Responses
```python
      def http_response(body: str, status: str = "200 OK") -> bytes:
          response = (
              f"HTTP/1.1 {status}\r\n"
              "Content-Type: text/html; charset=utf-8\r\n"
              f"Content-Length: {len(body.encode('utf-8'))}\r\n"
              "\r\n"
              f"{body}"
          )
          return response.encode("utf-8")
```
Builds a minimal HTTP response with headers and body.

## Handling Clients
```python
      def handle_client(client_socket: socket.socket) -> None:
          request = client_socket.recv(1024).decode("utf-8", errors="ignore")
          path = parse_http_path(request)
          # route handling...
          client_socket.sendall(response)
          client_socket.close()
```
Reads the client request, determines the response, and closes the connection.

## Learning Goals

 - Understand how sockets work in Python
 - Learn how HTTP requests and responses are structured
 - See how routing can be implemented in its simplest form
 - Prepare for more advanced servers using asyncio, decorators, or templates

__This project is toy code for educational purposes. It is intentionally simple to highlight the core mechanics of a web server.__