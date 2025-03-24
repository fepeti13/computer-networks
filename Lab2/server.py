import socket
import threading
import os
import mimetypes
import time

HOST = 'localhost'
PORT = 12000
WEB_ROOT = "webroot"
TIMEOUT = 5
SUPPORTED_MIME_TYPES = {
    "text/plain",
    "text/html",
    "text/css",
    "image/jpeg",
    "image/png",
    "video/mp4",
}

def handle_client(client_socket, addr):
    thread_id = threading.get_ident()
    print(f"[Thread {thread_id}] New connection from {addr}")

    client_socket.settimeout(TIMEOUT)
    keep_alive = True

    while keep_alive:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            request_line = request.split("\n")[0]
            print(f"[Thread {thread_id}] Received request: {request_line}")

            parts = request_line.split()
            if len(parts) < 2:
                break  

            method, path = parts[0], parts[1]

            if method != "GET":
                send_response(client_socket, "405 Method Not Allowed", "text/plain", "Only GET supported", keep_alive)
                break

            if path == "/":
                path = "/index.html"

            file_path = os.path.join(WEB_ROOT, path.lstrip("/"))
            connection_header = get_header_value(request, "Connection")

            keep_alive = connection_header.lower() == "keep-alive" if connection_header else False

            if os.path.isfile(file_path):
                send_file(client_socket, file_path, keep_alive)
            else:
                send_response(client_socket, "404 Not Found", "text/html", "<h1>404 File Not Found</h1>", keep_alive)

        except socket.timeout:
            print(f"[Thread {thread_id}] Connection timed out")
            break

    print(f"[Thread {thread_id}] Closing connection")
    client_socket.close()

def send_file(client_socket, file_path, keep_alive):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type not in SUPPORTED_MIME_TYPES:
        send_response(client_socket, "415 Unsupported Media Type", "text/plain", "Unsupported file type", keep_alive)
        return

    with open(file_path, "rb") as f:
        content = f.read()

    headers = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Type: {mime_type}\r\n"
        f"Content-Length: {len(content)}\r\n"
        f"Connection: {'keep-alive' if keep_alive else 'close'}\r\n"
        "\r\n"
    )

    client_socket.send(headers.encode() + content)

def send_response(client_socket, status, content_type, body, keep_alive):
    response = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"Connection: {'keep-alive' if keep_alive else 'close'}\r\n"
        "\r\n"
        f"{body}"
    )
    client_socket.send(response.encode())

def get_header_value(request, header_name):
    for line in request.split("\n"):
        if line.lower().startswith(header_name.lower() + ":"):
            return line.split(":", 1)[1].strip()
    return None

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server running on http://{HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    os.makedirs(WEB_ROOT, exist_ok=True)
    start_server()
