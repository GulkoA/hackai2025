from humanoid import Humanoid, Context, Inventory, Action

class HumanoidManager():
    def __init__(self):
        # maps id to Humanoid
        self.humanoids: dict[int, Humanoid] = {}
        self.server = None

    def server_command(self, id, command: str, parameters: dict):
        if self.server:
            self.server.send_command(id, command, parameters)

    def prompt_agent_action(self, id, ctx):
        context = Context.model_validate_json(ctx)

        if id not in self.humanoids:
            # create new agent
            self.humanoids[id] = Humanoid(
                ai_model='llama3.2',
                id=id,
                name=f"Agent{id}",
                occupation="farmer",
            )

        action: Action = self.humanoids[id].prompt_agent_action(context)
        if action.action.startswith("walk"):
            dest = action.action.split("_")[-1]
            self.server_command(id, "walk", dest)
        elif action.action.startswith("talk"):
            partner_name = action.action.split("_")[-1]
            partner_id = next((k for k, v in self.humanoids.items() if v.name == partner_name), None)
            self.server_command(id, "talk", partner_id)
        else:
            self.server_command(id, action.action, action.intention)

    
    def prompt_agent_conversation(self, id, partner_id: int, phrase: str, ctx: dict, trade_offer: dict, trade_receive: dict):
        partner_name = self.humanoids[partner_id].name
        context = Context.model_validate_json(ctx)
        offer = Inventory.model_validate_json(trade_offer)
        receive = Inventory.model_validate_json(trade_receive)
        return self.humanoids[id].prompt_agent_conversation(partner_name, phrase, context, offer, receive)
    
    def end_conversation(self, id, ctx):
        context = Context.model_validate(ctx)
        return self.humanoids[id].end_conversation(context)
    
    def handle_command(self, id, command: str, parameters: dict):
        if command == "prompt_agent_action":
            return self.prompt_agent_action(id, parameters["ctx"])
        elif command == "prompt_agent_conversation":
            return self.prompt_agent_conversation(id, parameters["partner_id"], parameters["phrase"], parameters["ctx"], parameters["trade_offer"], parameters["trade_receive"])
        elif command == "end_conversation":
            return self.end_conversation(id, parameters["ctx"])
