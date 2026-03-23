# 🧠 LangGraph — Clear Explanation

## What is LangGraph?
LangGraph is a workflow controller for AI systems.

It controls:
- steps
- execution order
- data flow

---

## Without LangGraph
messages → LLM → response

No control, no structure.

---

## With LangGraph
START → Node → END

---

## Key Concepts

### State
Data passed between steps:
{
  "messages": [...]
}

### Node
Function:
- takes state
- returns updated state

### Graph
Defines flow

---

## Chatbot Flow
User → API → Graph → Node → LLM → Response

---

## Important

LLM generates answers  
LangGraph controls flow  

---

## Why use it?

- structured system
- scalable (RAG later)
- production mindset

---

## Future
Add retrieval node → becomes RAG

---

## Final
LangGraph = control system for AI
