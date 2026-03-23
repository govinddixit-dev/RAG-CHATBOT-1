from langgraph.graph import StateGraph
from state import ChatState
from nodes import retriever_node, chatbot_node

builder = StateGraph(ChatState)

builder.add_node("retriever", retriever_node)
builder.add_node("chatbot", chatbot_node)

builder.set_entry_point("retriever")
builder.add_edge("retriever", "chatbot")
builder.set_finish_point("chatbot")

graph = builder.compile()
