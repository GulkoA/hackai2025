import socket
import json
import asyncio
import time
from humanoid_manager import HumanoidManager

class WebsocketServer:
  def __init__(self, manager):
      self.manager = manager
      self.conn = None

  async def start_server(self):
      server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      try:
          server_socket.bind(('localhost', 12345))
          server_socket.listen(1)
          print("Server started, waiting for connection...")
      except Exception as e:
          print(f"Failed to start server: {e}")
          return

      try:
          self.conn, addr = server_socket.accept()
          # self.send_command(0, "start_walk", "dock")
          while True:
              data = self.conn.recv(1024)
              if not data:
                  break
              print(f"Received: {data.decode()}")
              self.receive_command(data.decode())
      except Exception as e:
          print(f"Server error: {e}")
      finally:
          self.conn.close()
          server_socket.close()

  def receive_command(self, message):
      obj = json.loads(message)
      command = obj["command"]
      parameters = obj["parameters"]
      id = obj["id"]
      print(f"Received command: {command}, parameters: {parameters}, id: {id}")

      self.manager.handle_command(id, command, parameters)

  def send_command(self, id, command, parameters):
      data = {
          "id": id,
          "command": command,
          "parameters": parameters
      }
      message = json.dumps(data)
      self.conn.sendall(message.encode())
      print(f"Sent: {message}")

if __name__ == "__main__":
    manager = HumanoidManager()
    server = WebsocketServer(manager)
    asyncio.run(server.start_server())

    # time.sleep(10)