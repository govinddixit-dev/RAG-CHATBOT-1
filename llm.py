import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()  # loads .env for local dev (Docker injects vars directly)

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)
