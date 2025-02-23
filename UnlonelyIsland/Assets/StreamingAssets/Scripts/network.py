import socket
import struct
import json

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
        data = {
            "id": 0,
            "destination": "housing"
        }
        message = json.dumps(data)
        conn.sendall(message.encode())
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            # Decode the message
            message = data.decode()
            print(f"Received: {message}")
            request = json.loads(message)

            # Process the request
            if request["action"] == "start_walk":
                start_walk(request["id"], request["dest"])
            elif request["action"] == "start_action":
                start_action(request["id"], request["action_type"])
            elif request["action"] == "start_conversation":
                start_conversation(request["id"], request["partner_id"])
            elif request["action"] == "say_in_conversation":
                say_in_conversation(request["id"], request["partner_id"], request["phrase"], request["stop"], request["trade_offer"], request["trade_receive"])
            else:
                print("Unknown action requested.")

            # Echo back the received data for confirmation
            conn.sendall(data)

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        conn.close()
        server_socket.close()

# Implementation of the requested functions

def start_walk(id: int, dest: str):
    print(f"Moving character with ID {id} to {dest}")

def start_action(id: int, action: str):
    print(f"Character {id} is performing action: {action}")

def start_conversation(id: int, partner_id: int):
    print(f"Starting conversation between {id} and {partner_id}")

def say_in_conversation(id: int, partner_id: int, phrase: str, stop: bool, trade_offer: list, trade_receive: list):
    print(f"Character {id} says to {partner_id}: {phrase}")
    print(f"Stop conversation: {stop}")
    print(f"Trade Offer: {trade_offer}")
    print(f"Trade Receive: {trade_receive}")

if __name__ == "__main__":
    start_server()
