from humanoid import Humanoid, Context, Inventory

class HumanoidManager():
  def __init__(self):
    # maps id to Humanoid
    self.humanoids: dict[int, Humanoid] = {}


  def prompt_agent_action(self, id, ctx):
    context = Context.model_validate_json(ctx)
    return self.humanoids[id].prompt_agent_action(context)
  
  def prompt_agent_conversation(self, partner_id: int, phrase: str, ctx: dict, trade_offer: dict, trade_receive: dict):
    partner_name = self.humanoids[partner_id].name
    context = Context.model_validate_json(ctx)
    offer = Inventory.model_validate_json(trade_offer)
    receive = Inventory.model_validate_json(trade_receive)
    return self.humanoids[id].prompt_agent_conversation(partner_name, phrase, context, offer, receive)
  
  def end_conversation(self, id, ctx):
    context = Context.model_validate(ctx)
    return self.humanoids[id].end_conversation(context)