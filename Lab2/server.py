#Ferencz Peter, fpim2346, lab2 halozatok
import socket
import threading
import time

HOST = 'localhost'
PORT = 12000
TIMEOUT = 5

MIME_TYPES = {
    "html": "text/html",
    "txt": "text/plain",
    "css": "text/css",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "mp4": "video/mp4"
}

def get_mime_type(filename):
    parts = filename.split(".")
    ext = parts[-1].lower() if len(parts) > 1 else ""
    return MIME_TYPES.get(ext, "application/octet-stream")

def read_file(filename):
    try:
        with open(filename, "rb") as f:
            return f.read()
    except:
        return None

def parse_request(request):
    lines = request.split("\r\n")
    if len(lines) < 1:
        return None, None
    
    parts = lines[0].split()
    if len(parts) < 2:
        return None, None

    return parts[0], parts[1]

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
            
            print(f"[Thread {thread_id}] Received request:\n{request}")

            method, path = parse_request(request)
            if method != "GET":
                response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nOnly GET supported"
                client_socket.send(response.encode())
                break

            if path == "/":
                path = "/index.html"

            path = path.lstrip("/")
            connection_header = "keep-alive" in request.lower()
            keep_alive = connection_header

            content = read_file(path)
            if content:
                mime_type = get_mime_type(path)
                response_headers = (
                    "HTTP/1.1 200 OK\r\n"
                    f"Content-Type: {mime_type}\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    f"Connection: {'keep-alive' if keep_alive else 'close'}\r\n"
                    "\r\n"
                )
                client_socket.send(response_headers.encode() + content)
            else:
                response_body = "<h1>404 File Not Found</h1>"
                response_headers = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    f"Connection: {'keep-alive' if keep_alive else 'close'}\r\n"
                    "\r\n"
                    f"{response_body}"
                )
                client_socket.send(response_headers.encode())

        except socket.timeout:
            print(f"[Thread {thread_id}] Connection timed out")
            break

    print(f"[Thread {thread_id}] Closing connection")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Server is running...")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

start_server()
