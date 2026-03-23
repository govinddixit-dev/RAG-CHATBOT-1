from typing import TypedDict, List

class ChatState(TypedDict):
    messages: List[dict]
    context: str   # retrieved RAG context; empty string when no docs are loaded
