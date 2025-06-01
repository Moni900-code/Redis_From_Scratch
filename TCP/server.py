
#TCP Server for Redis-like functionality
import socket
import select
import logging
import os
import time

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


store = {}
server_start_time = time.time()

# Server info
def info():
    uptime = time.time() - server_start_time
    info_str = (
        f"Redis-Scratch Server\n"
        f"Uptime: {int(uptime)} seconds\n"
        f"Keys stored: {len(store)}\n"
    )
    return info_str

# Main server loop
def start_server(host='0.0.0.0', port=6379):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    server_socket.setblocking(False)

    sockets_list = [server_socket]
    clients = {}

    logging.info(f"Server started on {host}:{port}")
    print(f"[+] Server listening on {host}:{port}...")

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                client_socket.setblocking(False)
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
                logging.info(f"Accepted new connection from {client_address}")
            else:
                try:
                    data = notified_socket.recv(1024).decode().strip()
                    if not data:
                        raise ConnectionResetError

                    logging.info(f"Command from {clients[notified_socket]}: {data}")
                    parts = data.split()

                    if len(parts) == 0:
                        response = "ERROR: Empty command"
                    else:
                        cmd = parts[0].upper()
                        if cmd == 'SET' and len(parts) == 3:
                            store[parts[1]] = parts[2]
                            response = "OK"
                        elif cmd == 'GET' and len(parts) == 2:
                            response = store.get(parts[1], "NULL")
                        elif cmd == 'DEL' and len(parts) == 2:
                            if parts[1] in store:
                                del store[parts[1]]
                                response = "1"
                            else:
                                response = "0"
                        elif cmd == 'EXISTS' and len(parts) == 2:
                            response = "1" if parts[1] in store else "0"
                        elif cmd == 'PING':
                            response = "PONG"
                        elif cmd == 'INFO':
                            response = info()
                        elif cmd == 'FLUSHALL':
                            store.clear()
                            response = "OK"
                        elif cmd == 'EXIT':
                            response = "BYE"
                            notified_socket.send((response + "\n").encode())
                            raise ConnectionResetError
                        else:
                            response = "ERROR: Invalid command"

                    notified_socket.send((response + "\n").encode())

                except Exception as e:
                    logging.info(f"Closed connection from {clients[notified_socket]}: {e}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    notified_socket.close()

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
            notified_socket.close()

if __name__ == '__main__':
    start_server()