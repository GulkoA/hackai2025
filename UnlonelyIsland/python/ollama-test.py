from humanoid import Humanoid

agent = Humanoid(
  model='deepseek-r1',
  name='Steeve',
  occupation='farmer',
)

agent.select_action("What would you like to do?", actions_available=[], conversations_available=[])
