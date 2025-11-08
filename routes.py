from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime, timedelta
import random

from database import create_document, get_documents
from schemas import Trip, Preference

router = APIRouter(prefix="/api")

class PlanRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Natural-language trip request")
    user_id: Optional[str] = Field(None, description="User identifier for personalization")

class RouteOption(BaseModel):
    mode: Literal['cab','metro','bus','train','auto','flight']
    provider: str
    price: float
    currency: str = 'INR'
    duration_minutes: int
    eta: str
    legs: Optional[List[dict]] = None

class PlanResponse(BaseModel):
    query: str
    options: List[RouteOption]

@router.post('/plan', response_model=PlanResponse)
async def plan_trip(payload: PlanRequest):
    # Mock AI planning: generate a few route options with randomized but deterministic-ish values
    random.seed(payload.query)
    providers_by_mode = {
        'cab': ['Uber', 'Ola'],
        'metro': ['DMRC'],
        'bus': ['DTC'],
        'train': ['IRCTC'],
        'auto': ['Rapido'],
        'flight': ['IndiGo', 'Air India']
    }
    candidate_modes = ['cab','metro','bus','train']
    options: List[RouteOption] = []
    now = datetime.now()
    for m in candidate_modes:
        provider = random.choice(providers_by_mode[m])
        base = random.uniform(120, 900)
        dur = random.randint(20, 120)
        eta = (now + timedelta(minutes=dur)).strftime('%I:%M %p')
        option = RouteOption(
            mode=m,
            provider=provider,
            price=round(base, 2),
            duration_minutes=dur,
            eta=eta,
        )
        options.append(option)

    # Multi-modal example
    options.append(RouteOption(
        mode='metro',
        provider='DMRC+Uber',
        price=round(random.uniform(150, 450), 2),
        duration_minutes=random.randint(35, 95),
        eta=(now + timedelta(minutes=random.randint(35,95))).strftime('%I:%M %p'),
        legs=[
            {"mode":"metro","line":"Blue Line","duration":30},
            {"mode":"cab","provider":"Uber","duration":12}
        ]
    ))

    return PlanResponse(query=payload.query, options=options)

class BookRequest(BaseModel):
    user_id: str
    query: str
    selection: RouteOption
    origin: Optional[str] = None
    destination: Optional[str] = None
    return_trip: Optional[bool] = False

@router.post('/book')
async def book_trip(req: BookRequest):
    trip = Trip(
        user_id=req.user_id,
        query=req.query,
        origin=req.origin,
        destination=req.destination,
        mode=req.selection.mode,
        provider=req.selection.provider,
        price=req.selection.price,
        currency=req.selection.currency,
        duration_minutes=req.selection.duration_minutes,
        eta=req.selection.eta,
        return_trip=req.return_trip,
        status='confirmed',
        legs=req.selection.legs
    )
    inserted_id = create_document('trip', trip)
    return {"ok": True, "id": inserted_id}

@router.get('/trips')
async def list_trips(user_id: Optional[str] = None, limit: int = 50):
    filt = {"user_id": user_id} if user_id else {}
    docs = get_documents('trip', filt, limit=limit)
    # Convert ObjectId to string for JSON safety
    for d in docs:
        if '_id' in d:
            d['_id'] = str(d['_id'])
        if 'created_at' in d:
            d['created_at'] = d['created_at'].isoformat() if hasattr(d['created_at'], 'isoformat') else d['created_at']
        if 'updated_at' in d:
            d['updated_at'] = d['updated_at'].isoformat() if hasattr(d['updated_at'], 'isoformat') else d['updated_at']
    return {"items": docs}

class PreferenceRequest(Preference):
    pass

@router.get('/preferences')
async def get_preferences(user_id: str):
    docs = get_documents('preference', {"user_id": user_id}, limit=1)
    pref = docs[0] if docs else None
    if pref and '_id' in pref:
        pref['_id'] = str(pref['_id'])
    return {"item": pref}

@router.post('/preferences')
async def set_preferences(payload: PreferenceRequest):
    inserted_id = create_document('preference', payload)
    return {"ok": True, "id": inserted_id}
