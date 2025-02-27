import socket
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AI Scripts')))

from humanoid_manager import HumanoidManager

def start_server(manager):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('localhost', 12345))
        server_socket.listen(1)
        print("Server started, waiting for connection...")
    except Exception as e:
        print(f"Failed to start server: {e}")
        return

    try:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")
            try:
                # Parse the JSON message
                message = data.decode()
                command_obj = json.loads(message)
                manager.handle_command(command_obj["id"], command_obj["command"], command_obj["parameters"])
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
            conn.sendall(data)
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    manager = HumanoidManager()
    start_server(manager)