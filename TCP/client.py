# TCP Client for Redis-like interaction
import socket
import json
import readline

# Client connection
def start_client(host='tcp-server', port=6379, json_mode=True):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"[+] Connected to TCP server at {host}:{port}")
    print(f"[i] JSON Output: {'ON' if json_mode else 'OFF'}")

    try:
        while True:
            cmd = input("Client> ").strip()
            if not cmd:
                continue
            client.send(cmd.encode())
            response = client.recv(1024).decode().strip()
            if json_mode:
                result = {"command": cmd, "response": response}
                print(json.dumps(result, indent=2))
            else:
                print("Server>", response)
            if cmd.upper() == 'EXIT':
                print("[x] Closing connection.")
                break
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        client.close()

if __name__ == '__main__':
    start_client()