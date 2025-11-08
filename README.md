# TripMind – FastAPI Backend

Production-ready FastAPI backend for TripMind – Your Autonomous Travel Agent.

## Features
- REST APIs for planning, booking, trips history, and preferences
- MongoDB persistence via environment variables (DATABASE_URL, DATABASE_NAME)
- CORS enabled for easy frontend integration
- Pydantic validation for all payloads
- Simple modular structure

## Endpoints
- POST `/api/plan` – natural language planning -> returns mock AI route suggestions
- POST `/api/book` – save a booking
- GET `/api/trips?user_id=USER&limit=50` – list trips
- GET `/api/preferences?user_id=USER` – fetch preferences
- POST `/api/preferences` – create/update preferences

## Run locally
1. Create `.env` with:
```
DATABASE_URL=mongodb+srv://<user>:<pass>@cluster.mongodb.net
DATABASE_NAME=tripmind
PORT=8000
```
2. Install deps and run:
```
pip install -r requirements.txt
python main.py
```

## Replit
- Replit automatically loads `.env`. Ensure DATABASE_URL and DATABASE_NAME are set in Secrets.
- Expose port 8000.

## Notes
- The `/api/plan` endpoint returns realistic mock options. Swap it with a real AI service later.
- Collections are inferred from model names (lowercased). E.g., Trip -> `trip`, Preference -> `preference`.
