from ollama import ChatResponse, chat
import rich
from pydantic import BaseModel
import numpy as np

locations_descriptions = {
    'dock': 'Walk to the fishing dock where you can catch fish',
    'farm': 'Walk to the farm where you can grow tomatoes and other vegetables',
    'housing': 'Walk to the housing area where you can rest and recover your energy',
    'market': 'Walk to the market where you can trade goods and cook meals',
}

action_descriptions = {
    'start_fishing': 'Start fishing at the dock',
    'start_farming': 'Start farming at the farm',
    'sleep': 'Go to sleep at the housing area',
}

class Action(BaseModel):
    action: str
    intention: str
    mood: str

class Humanoid():
    def __init__(self, model: str, name, occupation):
        self.model = model
        self.name = name
        self.occupation = occupation
        self.personality_vector = np.random.rand(5)
        self.vitals = {
            'hunger': 0.1, # more hungry = wants to eat
            'stamina': 1, # more stamina = more energy
        }
        self.inventory = {
            'fish': 0,
            'tomatoes': 0,
            'gold': 100,
        }
        self.location = 'farm'
        self.relations_summary = {
            "You have no friends yet"
        }
        self.lifetime_summary = {
            "You were just born"
        }
        self.yesterday_summary = {
            "You did not exist yesterday"
        }

        self.history = {
            'context': [ 
            ],
            'conversation': [],
        }

    def summary_prompt(self):
        return f"""
        You are {self.name}, a {self.occupation} on the mechanical island. You can walk, interact with other humanoids, and trade fish, tomatoes, and buy food at the market. Your goal is to survive and thrive on the island.
        You have {self.inventory['fish']} fish, {self.inventory['tomatoes']} tomatoes, and {self.inventory['gold']} gold.
        You are at the {self.location}.
        Your hunger: {self.vitals['hunger']} (you are {1 - self.vitals['hunger']} full)
        Your stamina: {self.vitals['stamina']} (you are {self.vitals['stamina'] * 100}% energetic)

        Lifetime: {self.lifetime_summary}
        Yesterday: {self.yesterday_summary}
        Relations: {self.relations_summary}
        """

    def generate_action_format(self, actions_available, conversations_available):
        available_action_descriptions = {}
        for location, description in locations_descriptions.items():
            available_action_descriptions[f"walk_to_{location}"] = description
        for conversation in conversations_available:
            available_action_descriptions[f"start_conversation_{conversation}"] = f"Start a conversation with {conversation}"
        for action in actions_available:
            available_action_descriptions[action] = action

        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": list(available_action_descriptions.keys()),
                    "description": "\n".join([f"- {k}: {v}" for k, v in available_action_descriptions.items()]),
                },
                "intention": {
                    "type": "string",
                    "description": "Why did you decide to do this action? Be as descriptive and specific as possible.",
                    "minLength": 25,
                },
                "mood": {
                    "type": "string",
                    "description": "How does this situation make you feel?",
                    "enum": ["happy", "sad", "angry", "neutral"],
                }
            },
            "required": ["intention", "mood", "action"],
            "additionalProperties": False,
        }

    def select_action(self, message, actions_available, conversations_available):
        messages = [
            *self.history['context'],
            *self.history['conversation'],
            {'role': 'system', 'content': self.summary_prompt()},
            {'role': 'user', 'content': message},
        ]

        response: ChatResponse = chat(
            'llama3.2',
            messages=messages,
            format=self.generate_action_format(actions_available, conversations_available),
        )

        try:
            action_data = Action.model_validate_json(response.message.content)
            print('Intention:', action_data.intention)
            print('Mood:', action_data.mood)
            print('Performing action:', action_data.action)
        except Exception as e:
            print('Invalid action format in response:', response.message.content, e)

        return action_data
