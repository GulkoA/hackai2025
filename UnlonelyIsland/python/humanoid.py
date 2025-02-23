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

class Inventory(BaseModel):
    fish: int
    tomatoes: int
    meals: int
    gold: int

class Vitals(BaseModel):
    hunger: int
    stamina: int

class Conversation(BaseModel):
    content: str
    mood: str
    action: str
    trade_offer: Inventory
    trade_receive: Inventory


class Context(BaseModel):
    inventory: Inventory
    vitals: Vitals
    location: str
    agents_nearby: list[int]
    actions_available: list[str]

class PsycologicalPortrait(BaseModel):
    mood: str

class Humanoid():
    def __init__(self, ai_model: str, id: str, name: str, occupation: str):
        self.ai_model = ai_model
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
        self.partner = None

    def prompt_agent_action(self, context: Context):
        """
        Prompt agent to generate the next action
        """

        def summary_prompt(context: Context):
            return f"""
            You are {self.name}, a {self.occupation} on the mechanical island. You can walk, interact with other humanoids, and trade fish, tomatoes, and buy food at the market. You CANNOT eat raw fish or tomatoes, only cooked meals. Your goal is to survive and thrive on the island.
            You have {context.inventory.fish} fish, {context.inventory.tomatoes} tomatoes, and {context.inventory.gold} gold. THERE ARE NO OTHER RESOURCES AVAILABLE.
            Your hunger: {context.vitals.hunger} (you are {100 - context.vitals.hunger * 100}% full)
            Your stamina: {context.vitals.stamina} (you are {context.vitals.stamina * 100}% energetic)

            Lifetime: {self.lifetime_summary}
            Yesterday: {self.yesterday_summary}
            Relations: {self.relations_summary}

            You are at the {context.location}. Decide what to do next based on your personality.
            """
        
        def generate_action_format(actions_available, conversations_available):
            actions = {}
            for location, description in locations_descriptions.items():
                actions[f"walk_to_{location}"] = description
            for conversation in conversations_available:
                actions[f"talk_to_{conversation}"] = f"Start a conversation with {conversation}"
            for action in actions_available:
                actions[action] = action_descriptions[action]

            return {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": list(actions.keys()),
                        "description": "\n".join([f"- {k}: {v}" for k, v in actions.items()]),
                    },
                    "intention": {
                        "type": "string",
                        "description": "Why did you decide to do this action? Be as descriptive and specific as possible. Use verbal informal natural language",
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


        messages = [
            *self.history['actions'],
            {'role': 'system', 'content': summary_prompt(context)},
        ]

        response: ChatResponse = chat(
            model=self.ai_model,
            messages=messages,
            format=generate_action_format(context.actions_available, context.agents_nearby),
        )

        try:
            action_data = Action.model_validate_json(response.message.content)
            print(f"Model decided to {action_data.action} because {action_data.intention} and feels {action_data.mood}")
        except Exception as e:
            print('Invalid action format in response:', response.message.content, e)

        self.history['actions'].append({
            'role': 'assistant',
            'content': f"I decided to {action_data.action} because {action_data.intention}",
        })

        return action_data

    def prompt_agent_conversation(self, partner_name: str, phrase: str, ctx: Context, trade_offer: Inventory, trade_receive: Inventory):
        """
        Prompt agent to generate next phrase in a conversation
        Only applicable when conversation is running

        Args:
            partner_name: Name of the partner in the conversation
            ctx: Context of the agent
            trade_offer: Items offered to me
            trade_receive: Items I will give in return
        """

        def summary_prompt(ctx: dict):
            trade = ""
            if sum(trade_offer.model_dump().values(), trade_receive.model_dump().values()) > 0:
                trade = f"They offered a trade: {", ".join([f"{k}: {v}" for k, v in trade_offer.model_dump().items() if v > 0])} for {", ".join([f"{k}: {v}" for k, v in trade_receive.model_dump().items() if v > 0])}"
            return f"""
            You are {self.name}, a {self.occupation} on the mechanical island. You can walk, interact with other humanoids, and trade fish, tomatoes, and buy food at the market. You CANNOT eat raw fish or tomatoes, only cooked meals. Your goal is to survive and thrive on the island.
            You have {ctx.inventory.fish} fish, {ctx.inventory.tomatoes} tomatoes, and {ctx.inventory.gold} gold. THERE ARE NO OTHER RESOURCES AVAILABLE.
            Your hunger: {ctx.vitals.hunger} (you are {100 - ctx.vitals.hunger * 100}% full)
            Your stamina: {ctx.vitals.stamina} (you are {ctx.vitals.stamina * 100}% energetic)

            Lifetime: {self.lifetime_summary}
            Yesterday: {self.yesterday_summary}
            Relations: {self.relations_summary}
            
            You are at the {ctx['location']} conversing with {partner_name}. {trade} They said {phrase} Decide what to say next based on your personality.
            """
        
        def generate_conversation_format(inventory: Inventory):
            actions = ["end_conversation", "continue_conversation"]
            description = "End the conversation immediately or continue talking"
            if sum(ctx.trade_offer.model_dump().values(), ctx.trade_receive.model_dump().values()) > 0:
                actions.update(["accept_trade"])
                description += " or accept the trade offer (note that accepting trade will stop the conversation)"
            return {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "What do you want to say to the other person?",
                        "minLength": 25,
                    },
                    "mood": {
                        "type": "string",
                        "description": "How does this situation make you feel?",
                        "enum": ["happy", "sad", "angry", "neutral"],
                    },
                    "action": {
                        "type": "string",
                        "enum": actions,
                    },
                    "trade_offer": {
                        "type": "object",
                        "properties": {
                            "fish": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": inventory.fish,
                            },
                            "tomatoes": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": inventory.tomatoes,
                            },
                            "meals":{
                                "type": "integer",
                                "minimum": 0,
                                "maximum": inventory.meals,
                            },
                            "gold": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": inventory.gold,
                            },
                        },
                        "required": [],
                        "additionalProperties": False,
                    },
                    "trade_receive": {
                        "type": "object",
                        "properties": {
                            "fish": {
                                "type": "integer",
                                "minimum": 0,
                            },
                            "tomatoes": {
                                "type": "integer",
                                "minimum": 0,
                            },
                            "meals":{
                                "type": "integer",
                                "minimum": 0,
                            },
                            "gold": {
                                "type": "integer",
                                "minimum": 0,
                            },
                        },
                        "required": [],
                        "additionalProperties": False,
                    },
                },
                "required": ["content", "intention", "mood", "action"],
                "additionalProperties": False,
            }
    
        self.partner = partner_name

        messages = [
            *self.history['conversation'],
            {'role': 'system', 'content': summary_prompt(ctx)},
        ]

        response: ChatResponse = chat(
            model=self.ai_model,
            messages=messages,
            format=generate_conversation_format(ctx.inventory),
        )

        try:
            conversation_data = Conversation.model_validate_json(response.message.content)
            print(f"Model decided to say {conversation_data.content} and feels {conversation_data.mood}")
        except Exception as e:
            print('Invalid conversation format in response:', response.message.content, e)

        return conversation_data
  
    def end_conversation(self):
        """
        Finalize the conversation with the partner
        """
        summary_messages = [
            *self.history['conversation'],
            {'role': 'system', 'content': "The conversation has ended, make an executive summary of the conversation."},
        ]
        summary = chat(
            model=self.ai_model,
            messages=summary_messages,
            format={"type": "object", "properties": {"summary": {"type": "string"}}},
        )
        self.history['conversation'] = []
        print(f"Conversation ended with summary: {summary.message.content}")
        self.history['actions'].append({
            'role': 'assistant',
            'content': f"The conversation with {self.partner} ended with summary: {summary.message.content}",
        })

        # return conversation_data

    def generate_character_context(self):
        
        response: ChatResponse = chat(
            model=self.ai_model,
            messages=[f'You are {self.name} who works as {self.occupation}. Based on the OCEAN personality model(the Big Five personality traits) your openness:{self.personality_vector[0]}, conscientiousness:{self.personality_vector[1]}, extraversion:{self.personality_vector[2]}, agreeableness:{self.personality_vector[3]}, and neuroticism:{self.personality_vector[4]}. Give a physcological portret for you.'],
        )

        try:
            conversation_data = PsycologicalPortrait.model_validate_json(response.message.content)
            print(f"Model feels {conversation_data.mood}")
        except Exception as e:
            print('Invalid conversation format in response:', response.message.content, e)

        return conversation_data
    