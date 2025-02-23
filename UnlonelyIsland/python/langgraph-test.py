import datetime
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_ollama import ChatOllama

from IPython.display import Image, display

from langchain.tools import tool

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

@tool
def current_time():
    """
    Returns the current time in HH:MM:SS format
    """
    print("Current time is", datetime.datetime.now().strftime("%H:%M:%S"))
    return datetime.datetime.now().strftime("%H:%M:%S")


graph_builder = StateGraph(State)

llm = ChatOllama(model="llama3.2")
model_with_tool = llm.bind_tools([current_time])

def chatbot(state: State):
    meta_prompt = "NOTE: Always use available tools whenever it enhances your answer."
    # Prepend the meta prompt to the existing messages.
    messages = [meta_prompt] + state["messages"]
    return {"messages": [model_with_tool.invoke(messages)]}


graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("current_time", ToolNode([current_time]))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition, {"current_time": "current_time", END: END})
graph_builder.add_edge("current_time", "chatbot")
# graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile(memory)
print(graph.get_graph().draw_mermaid())

# res = model_with_tool.invoke("what time is it rn?").tool_calls
# print(res)

# try:
#     i = Image(graph.get_graph().draw_mermaid_png())
#     display(i)
# except Exception:
#     # This requires some extra dependencies and is optional
#     pass

config = {"configurable": {"thread_id": "1"}}

def stream_graph_updates(user_input: str):
    response = graph.invoke({"messages": [user_input]}, config)
    # print(response)
    for message in response["messages"]:
        print(message)

while True:
    user_input = input("User: ")
    stream_graph_updates(user_input)