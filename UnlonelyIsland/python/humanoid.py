from ollama import ChatResponse, chat
import rich
from pydantic import BaseModel
import numpy as np
import dbm

locations_descriptions = {
    'dock': 'Walk to the fishing dock where you can catch fish if you are a fisherman',
    'farm': 'Walk to the farm where you can farm tomatoes if you are a farmer',
    'housing': 'Walk to the housing area where you can rest and recover your energy',
    'market': 'Walk to the market where you can trade goods and cook meals',
}

action_descriptions = {
    'start_fishing': 'Start fishing at the dock',
    'start_farming': 'Start farming at the farm',
    'start_cooking': 'Start cooking using tomatoes and fish. You need 1 tomato and 1 fish to cook a meal',
    'sleep': 'Go to sleep at the housing area',
}

class Action(BaseModel):
    action: str
    intention: str
    mood: str

class Context(BaseModel):
    inventory: dict[str, int] = {
        "fish": 0,
        "tomatoes": 0,
        "meals": 0,
        "gold": 0
    }
    vitals: dict[str, int] = {
        "hunger": 0,
        "stamina": 0
    }
    location: str
    agents_nearby: list[int]
    actions_available: list[str]

class Humanoid():
    def __init__(self, model: str, id: str, name: str, occupation: str):
        self.model = model
        self.id = id
        self.name = name
        self.occupation = occupation
        self.personality_vector = np.random.rand(5)
        
        self.lifetime_summary = {
            "You were just born"
        }
        self.yesterday_summary = {
            "You did not exist yesterday"
        }
        self.relations_summary = {
            "You have no relations yet"
        }

        self.history = {
            'actions': [],
            'conversation': [],
        }


    def summary_prompt(self, context: Context):
        return f"""
        You are {self.name}, a {self.occupation} on the mechanical island. You can walk, interact with other humanoids, and trade fish, tomatoes, and buy food at the market. You CANNOT eat raw fish or tomatoes, only cooked meals. Your goal is to survive and thrive on the island.
        You have {context.inventory['fish']} fish, {context.inventory['tomatoes']} tomatoes, and {context.inventory['gold']} gold. THERE ARE NO OTHER RESOURCES AVAILABLE.
        You are at the {context.location}.
        Your hunger: {context.vitals['hunger']} (you are {100 - context.vitals['hunger'] * 100}% full)
        Your stamina: {context.vitals['stamina']} (you are {context.vitals['stamina'] * 100}% energetic)

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

    def prompt_agent_action(self, context: Context):
        messages = [
            *self.history['actions'],
            {'role': 'system', 'content': self.summary_prompt(context)},
            {'role': 'user', 'content': "What would you like to do next? Please select the best action per your personality."},
        ]

        response: ChatResponse = chat(
            model=self.model,
            messages=messages,
            format=self.generate_action_format(context.actions_available, context.agents_nearby),
        )

        try:
            action_data = Action.model_validate_json(response.message.content)
            print('Intention:', action_data.intention)
            print('Mood:', action_data.mood)
            print('Performing action:', action_data.action)
        except Exception as e:
            print('Invalid action format in response:', response.message.content, e)

        return action_data
