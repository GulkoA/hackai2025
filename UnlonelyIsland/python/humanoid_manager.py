import asyncio
import json
import websockets
from humanoid import Humanoid, Context, Inventory

class HumanoidManager():
    def __init__(self):
        # maps id to Humanoid
        self.humanoids: dict[int, Humanoid] = {}
        self.websocket = None

    def prompt_agent_action(self, id, ctx):
        context = Context.model_validate_json(ctx)
        return self.humanoids[id].prompt_agent_action(context)
    
    def prompt_agent_conversation(self, id, partner_id: int, phrase: str, ctx: dict, trade_offer: dict, trade_receive: dict):
        partner_name = self.humanoids[partner_id].name
        context = Context.model_validate_json(ctx)
        offer = Inventory.model_validate_json(trade_offer)
        receive = Inventory.model_validate_json(trade_receive)
        return self.humanoids[id].prompt_agent_conversation(partner_name, phrase, context, offer, receive)
    
    def end_conversation(self, id, ctx):
        context = Context.model_validate(ctx)
        return self.humanoids[id].end_conversation(context)

    async def connect_ws(self, uri: str):
        self.websocket = await websockets.connect(uri)
        print("Connected to websocket server:", uri)
        # Start asynchronous listening for incoming messages.
        asyncio.create_task(self.listen_ws())
    
    async def send_command(self, id: int, command: str, parameters: dict):
        data = {
            "id": id,
            "command": command,
            "parameters": parameters
        }
        message = json.dumps(data)
        await self.websocket.send(message)

    async def listen_ws(self):
        while True:
            try:
                message = await self.websocket.recv()
            except websockets.ConnectionClosed:
                print("WebSocket connection closed")
                break
            print("Received message:", message)
            try:
                data = json.loads(message)
                cmd_id = data.get("id")
                command = data.get("command")
                parameters = data.get("parameters")
            except (json.JSONDecodeError, TypeError):
                print("Invalid message format")
                continue

            # Execute a command if a corresponding method exists.
            if hasattr(self, command):
                method = getattr(self, command)
                if asyncio.iscoroutinefunction(method):
                    result = await method(cmd_id, **parameters)
                else:
                    result = method(cmd_id, **parameters)
                print(f"Executed command {command} with result: {result}")
            else:
                print(f"Unknown command: {command}")

    async def close_ws(self):
        await self.websocket.close()

async def main():
    uri = "ws://localhost:12345"  # Change as needed
    manager = HumanoidManager()
    await manager.connect_ws(uri)
    # Run indefinitely.
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())