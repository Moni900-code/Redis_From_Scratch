import socket
import selectors

# --- Lab 1 Config ---
HOST = '0.0.0.0'
PORT = 6379

# --- Selector for single-threaded I/O multiplexing ---
sel = selectors.DefaultSelector()

# --- In-memory key-value store for REPL commands ---
store = {}

# --- Accept new client connections (Multiple Client Support) ---
def accept(sock):
    conn, addr = sock.accept()
    print(f"Connected by {addr}")
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

# --- Read client request and send response (Single-threaded request-response loop) ---
def read(conn):
    try:
        data = conn.recv(1024)
        if data:
            command_line = data.decode().strip()
            print(f"Received: {command_line}")
            response = handle_command(command_line)  # REPL-like command processing
            conn.sendall(response.encode())
        else:
            sel.unregister(conn)
            conn.close()
    except ConnectionResetError:
        sel.unregister(conn)
        conn.close()

# --- Command handler for PING, SET, GET ---
def handle_command(command_line):
    parts = command_line.split()
    if len(parts) == 0:
        return "-ERR empty command\r\n"

    cmd = parts[0].upper()

    if cmd == 'PING':
        return "+PONG\r\n"

    elif cmd == 'SET':
        if len(parts) != 3:
            return "-ERR wrong number of arguments for 'SET'\r\n"
        key, value = parts[1], parts[2]
        store[key] = value
        return "+OK\r\n"

    elif cmd == 'GET':
        if len(parts) != 2:
            return "-ERR wrong number of arguments for 'GET'\r\n"
        key = parts[1]
        value = store.get(key)
        if value is None:
            return "$-1\r\n"
        return f"${len(value)}\r\n{value}\r\n"

    else:
        return f"-ERR unknown command '{cmd}'\r\n"

# --- Main TCP server loop (Single-threaded event loop using selectors) ---
def main():
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print(f"Listening on {HOST}:{PORT}")
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()  # Single-threaded event polling
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)

if __name__ == "__main__":
    main()
