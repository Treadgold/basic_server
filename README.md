# Tiny Async Python HTML Server (Toy Example)

This repository contains **two intentionally minimal async web servers written in Python**.

They exist to answer one question clearly and honestly:

> **“What is a web server, really — and how do frameworks like Flask or FastAPI build on it?”**

No frameworks.  
No magic.  
No dependencies.  
Just Python, sockets, decorators, and a browser.

---

## What this project is (and is not)

### This *is*:
- A **learning-focused** web server implementation
- Small enough to understand end-to-end
- Written using only the Python standard library
- Designed for Python programmers at **all experience levels**
- A conceptual foundation for real-world web development

### This is *not*:
- Production-ready
- Secure against all attacks
- Fast or scalable
- A framework replacement

This is a **teaching tool**, not a deployment tool.

---

## Project structure


project/
│
├── basic_server.py
├── basic_server_v2.py
├── README.md
└── static/
├── index.html
└── about.html


- `basic_server.py` — the absolute minimum viable async HTTP server
- `basic_server_v2.py` — the same server, with routing decorators added
- `static/` — HTML files served directly to the browser

---

## Requirements

- Python 3.10+
- No third-party libraries

---

## Server 1: `basic_server.py`

### Purpose

`basic_server.py` is the **lowest-level useful example** of a web server.

It demonstrates:
- How a browser connects to a server
- What an HTTP request actually looks like
- How a URL maps to a file on disk
- How an HTTP response is manually constructed
- How async servers wait without blocking

There are **no decorators, no routing helpers, no abstractions**.

This is the “bare metal” version.

---

### How to run

```bash
python basic_server.py
```

Open a browser and navigate to

http://127.0.0.1:8000/

Edit static/index.html, refresh the browser — changes appear immediately.

### Conceptual flow

    Browser
      ↓
    HTTP request (text)
      ↓
    Python reads request
      ↓
    Path → file in ./static
      ↓
    File contents → HTTP response
      ↓
    Browser renders HTML


If you understand this file, you understand the foundation of web servers.

## Server 2: basic_server_v2.py

### Purpose

basic_server_v2.py introduces exactly one new idea: Routing decorators, like the ones used in Flask and FastAPI. Everything else stays almost the same.

This version exists to answer the question:

“How do frameworks turn URLs into Python functions?”

### What’s new in version 2

 - A global routes dictionary
 - A @route("/path") decorator
 - Functions registered as HTTP endpoints
 - Clear separation between:
   - framework code
   - application code

### Example route definition


    @route("/")
    def index() -> bytes:
        return load_html_file("index.html")


This decorator is doing something very simple:

    routes["/"] = index


That’s the entire trick.

### How to run

    python basic_server_v2.py


Then visit:

http://127.0.0.1:8000/
http://127.0.0.1:8000/about


Routes are mapped explicitly to HTML files, just like in real frameworks.

### Why this version matters

This is the moment where frameworks stop feeling magical.

You can now see that:

 - Decorators register functions at import time
 - Routing is just dictionary lookup
 - Frameworks mostly:
   -  organize code
   -  validate input
   -  protect against edge cases
   -  provide nicer APIs

They don’t change the fundamentals.

### How this maps to real frameworks

| This project           | Flask / FastAPI               |
| ---------------------- | ----------------------------- |
| `asyncio.start_server` | ASGI / WSGI server            |
| `handle_client()`      | Request lifecycle             |
| `routes` dict          | Router object                 |
| `@route()`             | `@app.route()` / `@app.get()` |
| Handler returns bytes  | Response objects              |
| Static file loading    | Templates / static files      |



### What’s intentionally missing

To keep the learning surface small, this project does not include:

 - Query strings
 - POST requests
 - JSON handling
 - MIME type detection
 - Middleware
 - Authentication
 - Error handling frameworks
 - Logging
 - Hot reload

Each of these is a separate layer that real frameworks add later.

### Suggested learning path

1. Read basic_server.py end-to-end
2. Run it and serve a real HTML file
3. Read basic_server_v2.py
4. Compare the decorator logic to Flask or FastAPI
5. Add:
    - a new route
    - a new HTML file
    - a simple handler returning a string

At that point, real web frameworks feel helpful, not confusing.

### Final note

If you understand these two files, you understand:

 - what a web server is
 - how requests become responses
 - how routing works
 - why frameworks exist

Everything else is just layers on top.