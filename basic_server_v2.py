import asyncio
from pathlib import Path
from typing import Callable, Dict, Optional

STATIC_DIR = Path("static")

# Type alias for route handlers
Handler = Callable[[], bytes]

# Route registry (this *is* the framework)
routes: Dict[str, Handler] = {}


def route(path: str) -> Callable[[Handler], Handler]:
    """
    Decorator used to register a function as a route handler.

    Example:
        @route("/")
        def index():
            ...
    """
    def decorator(func: Handler) -> Handler:
        routes[path] = func
        return func
    return decorator


def build_http_response(
    body: bytes,
    status: str = "200 OK",
    content_type: str = "text/html; charset=utf-8",
) -> bytes:
    """
    Build a minimal HTTP response.
    """
    headers: str = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body


def load_html_file(filename: str) -> Optional[bytes]:
    """
    Load an HTML file from the static directory.
    """
    file_path: Path = (STATIC_DIR / filename).resolve()

    if not file_path.is_relative_to(STATIC_DIR.resolve()):
        return None

    if file_path.exists() and file_path.is_file():
        return file_path.read_bytes()

    return None


def parse_http_path(request: str) -> str:
    """
    Extract the request path from the HTTP request line.
    """
    first_line: str = request.splitlines()[0]
    _, path, _ = first_line.split()
    return path


# --------------------------------------------------
# Route definitions (this is the part users write)
# --------------------------------------------------

@route("/")
def index() -> bytes:
    return load_html_file("index.html") or b"<h1>Missing index.html</h1>"


@route("/about")
def about() -> bytes:
    return load_html_file("about.html") or b"<h1>Missing about.html</h1>"


# --------------------------------------------------
# Server internals (this part rarely changes)
# --------------------------------------------------

async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
) -> None:
    """
    Handle a single HTTP client connection.
    """
    request_bytes: bytes = await reader.read(1024)
    request: str = request_bytes.decode("utf-8", errors="ignore")

    path: str = parse_http_path(request)

    handler: Optional[Handler] = routes.get(path)

    if handler is None:
        response = build_http_response(
            b"<h1>404 Not Found</h1>",
            status="404 Not Found",
        )
    else:
        body: bytes = handler()
        response = build_http_response(body)

    writer.write(response)
    await writer.drain()
    writer.close()


async def main() -> None:
    """
    Start the async server.
    """
    server = await asyncio.start_server(
        handle_client,
        host="127.0.0.1",
        port=8000,
    )

    addr = server.sockets[0].getsockname()
    print("Tiny async server with decorators")
    print(f"Open http://{addr[0]}:{addr[1]}")
    print("Press Ctrl+C to stop")

    async with server:
        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            print("\nShutting down gracefully...")


if __name__ == "__main__":
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("Server stopped.")
