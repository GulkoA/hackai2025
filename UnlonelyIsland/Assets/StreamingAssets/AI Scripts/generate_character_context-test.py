from humanoid import Humanoid

agent = Humanoid(
  ai_model='llama3.2',
  id='steeve',
  name='Steeve',
  occupation='farmer',
)
agent.generate_character_context()
# print(agent.generate_character_context())
