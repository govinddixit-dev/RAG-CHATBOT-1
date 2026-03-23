import os
import streamlit as st
import requests

API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="LangGraph Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 LangGraph Chatbot")
st.caption("Powered by LangGraph + Groq (llama-3.1) · FastAPI backend")

# ── sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    api_url = st.text_input("FastAPI URL", value=API_URL)

    st.divider()
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**How to run the backend**")
    st.code("uvicorn main:app --reload", language="bash")

    # live health check
    try:
        r = requests.get(f"{api_url}/health", timeout=2)
        if r.status_code == 200:
            data = r.json()
            st.success("Backend: online ✅")
            if data.get("rag_ready"):
                st.info("📚 RAG: documents loaded")
            else:
                st.caption("📂 RAG: no documents yet")
        else:
            st.error("Backend: error ❌")
    except Exception:
        st.warning("Backend: offline ⚠️")

    # PDF upload for RAG
    st.divider()
    st.subheader("📄 PDF Knowledge Base")
    uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"], label_visibility="collapsed")
    if uploaded_pdf:
        if st.button("📤 UPLOAD PDF"):
            with st.spinner("Indexing PDF…"):
                try:
                    resp = requests.post(
                        f"{api_url}/upload",
                        files={"file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")},
                        timeout=60,
                    )
                    resp.raise_for_status()
                    d = resp.json()
                    st.success(f"✅ {d['filename']} — {d['chunks']} chunks indexed")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot reach backend")
                except Exception as e:
                    st.error(f"Upload failed: {e}")
    if st.button("🗑️ Clear PDF", disabled=not (True)):
        try:
            r = requests.post(f"{api_url}/clear", timeout=5)
            r.raise_for_status()
            st.success("PDF index cleared")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to clear: {e}")

# ── chat state ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── render history ────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── user input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your message…"):
    # show user bubble immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # call FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                response = requests.post(
                    f"{api_url}/chat",
                    json={"messages": st.session_state.messages},
                    timeout=120,
                )
                response.raise_for_status()
                answer = response.json()["response"]
            except requests.exceptions.ConnectionError:
                answer = (
                    "❌ Cannot reach the backend. "
                    "Make sure `uvicorn main:app --reload` is running on port 8000."
                )
            except requests.exceptions.Timeout:
                answer = "⏳ The request timed out. The model might be loading — please try again."
            except Exception as exc:
                answer = f"❌ Unexpected error: {exc}"

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
