from llm import get_llm
import rag


def retriever_node(state):
    """Query the vector store if documents are loaded, skip otherwise."""
    if not rag.has_documents():
        return {"context": ""}
    messages = state.get("messages", [])
    last_user_msg = next(
        (m["content"] for m in reversed(messages) if m["role"] == "user"),
        "",
    )
    context = rag.retrieve(last_user_msg) if last_user_msg else ""
    return {"context": context}


def chatbot_node(state):
    """Call the LLM, injecting RAG context as a system message when available."""
    messages = list(state["messages"])
    context = state.get("context", "")

    if context:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant.\n"
                    "The user has uploaded a PDF document. Relevant excerpts from it are provided below.\n\n"
                    "Rules:\n"
                    "1. If the user's question is about the PDF content, answer using the excerpts below.\n"
                    "2. If the question is general (e.g. about yourself, the world, coding, etc.), answer from your own knowledge normally.\n"
                    "3. Never say you can't answer general questions because of the PDF.\n\n"
                    f"--- PDF EXCERPTS ---\n{context}\n--- END OF PDF EXCERPTS ---"
                ),
            }
        ] + messages
    else:
        messages = [{"role": "system", "content": "You are a helpful assistant."}] + messages

    response = get_llm().invoke(messages)
    return {
        "messages": state["messages"] + [
            {"role": "assistant", "content": response.content}
        ]
    }
