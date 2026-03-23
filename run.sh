#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# run.sh — start the chatbot stack
#
#   --docker   Use Docker Compose (Ollama + backend + frontend all in containers)
#   (no flag)  Run locally (requires Ollama installed & running separately)
# ─────────────────────────────────────────────────────────────────────────────

if [[ "$1" == "--docker" ]]; then
    echo "Starting full stack with Docker Compose..."
    docker compose up --build
else
    # Local mode — activate venv if present
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    elif [ -d "venv" ]; then
        source venv/bin/activate
    fi

    echo "Starting FastAPI backend on http://localhost:8000 ..."
    uvicorn main:app --reload --port 8000 &
    BACKEND_PID=$!

    echo "Starting Streamlit frontend on http://localhost:8501 ..."
    streamlit run streamlit_app.py --server.port 8501

    kill $BACKEND_PID 2>/dev/null
fi
