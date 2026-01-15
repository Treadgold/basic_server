import asyncio
from typing import Callable

Handler = Callable[[str], str]


def parse_http_path(request: str) -> str:
    """
    Extract the path from a very basic HTTP GET request.

    Example request line:
        GET /hello HTTP/1.1
    """
    first_line: str = request.splitlines()[0]
    _, path, _ = first_line.split()
    return path


def http_response(body: str, status: str = "200 OK") -> bytes:
    """
    Construct a minimal HTTP response.
    """
    response: str = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        "\r\n"
        f"{body}"
    )
    return response.encode("utf-8")


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    """
    Handle a single client connection.
    """
    request_bytes: bytes = await reader.read(1024)
    request: str = request_bytes.decode("utf-8", errors="ignore")

    path: str = parse_http_path(request)

    # --- routing (this is where Flask/FastAPI shine) ---
    if path == "/":
        body: str = "<h1>Hello, world!</h1>"
    elif path == "/about":
        body = "<h1>About</h1><p>Tiny async server.</p>"
    else:
        body = "<h1>404 Not Found</h1>"
        response: bytes = http_response(body, status="404 Not Found")
        writer.write(response)
        await writer.drain()
        writer.close()
        return

    response = http_response(body)
    writer.write(response)
    await writer.drain()
    writer.close()


async def main() -> None:
    """
    Start the async TCP server.
    """
    server = await asyncio.start_server(
        handle_client,
        host="127.0.0.1",
        port=8000,
    )

    addr = server.sockets[0].getsockname()
    print(f"Serving on http://{addr[0]}:{addr[1]}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
