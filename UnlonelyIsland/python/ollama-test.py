from humanoid import Humanoid

agent = Humanoid(
  model='deepseek-r1',
  id='steeve',
  name='Steeve',
  occupation='farmer',
)

agent.select_action("What would you like to do next?", actions_available=[], conversations_available=[])
