import socket

def start_server():
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
            conn.sendall(data)  # Echo back the received data
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()