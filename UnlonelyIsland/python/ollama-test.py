from agent import Agent

agent = Agent(
  model='deepseek-r1'
)

agent.chat("You are 10/10 full and 4/10 stamina. What would you like to do?", actions_available=[], conversations_available=[])
