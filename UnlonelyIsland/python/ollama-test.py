from humanoid import Humanoid, Context

agent = Humanoid(
  ai_model='deepseek-r1',
  id='steeve',
  name='Steeve',
  occupation='farmer',
)

ctx = Context(
  inventory={
    "fish": 0,
    "tomatoes": 0,
    "meals": 0,
    "gold": 0
  },
  vitals={
    "hunger": 0,
    "stamina": 1
  },
  location='housing',
  agents_nearby=[],
  actions_available=[]
)

agent.prompt_agent_action(ctx)

ctx.location = 'dock'
agent.prompt_agent_action(ctx)
