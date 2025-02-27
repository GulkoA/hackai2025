from humanoid import Humanoid, Context

agent_one = Humanoid(
  model='llama3.2',
  id='ct',
  name='Rex',
  occupation='cook',
)

agent_two = Humanoid(
  model='llama3.2',
  id='ben10',
  name='Ben',
  occupation='fisher',
)

ctx_1 = Context(
  inventory={
    "fish": 2,
    "tomatoes": 4,
    "meals": 2,
    "gold": 4
  },
  vitals={
    "hunger": 0.4,
    "stamina": 1
  },
  location='housing',
  agents_nearby=[],
  actions_available=['sleep', 'start_cooking']
)

ctx_2 = Context(
  inventory={
    "fish": 10,
    "tomatoes": 3,
    "meals": 0,
    "gold": 1
  },
  vitals={
    "hunger": 0.2,
    "stamina": 0.3
  },
  location='housing',
  agents_nearby=[],
  actions_available=['sleep', 'start_cooking']
)

# Todo: call functions(like Unity)

