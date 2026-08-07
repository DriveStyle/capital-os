#!/bin/bash
# Start Telegram Bot in background
python telegram/bot.py &

# Start FastAPI server on PORT provided by Render
uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}
