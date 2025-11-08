"""
Database Schemas for TripMind

Define MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- Preference -> "preference"
- Trip -> "trip"
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime


class Preference(BaseModel):
    """
    User travel preferences
    Collection name: "preference"
    """
    user_id: str = Field(..., description="Application user identifier")
    budget: Optional[float] = Field(None, ge=0, description="Typical max budget per trip")
    favorite_modes: Optional[List[Literal['cab', 'metro', 'bus', 'train', 'auto', 'flight']]] = Field(
        default=None, description="Preferred transport modes"
    )
    favorite_providers: Optional[List[str]] = Field(default=None, description="Preferred providers like Uber, Ola")
    time_windows: Optional[List[str]] = Field(
        default=None, description="Preferred time windows e.g. '08:00-10:00'"
    )
    home: Optional[str] = Field(None, description="Saved home location text")
    work: Optional[str] = Field(None, description="Saved work location text")
    notes: Optional[str] = Field(None, description="Additional user notes")


class Trip(BaseModel):
    """
    Booked trip document
    Collection name: "trip"
    """
    user_id: str = Field(..., description="Application user identifier")
    query: str = Field(..., description="Original natural-language query")
    origin: Optional[str] = Field(None, description="Origin location text")
    destination: Optional[str] = Field(None, description="Destination location text")
    mode: str = Field(..., description="Primary mode, e.g., cab, metro, train")
    provider: str = Field(..., description="Provider such as Uber, Ola, Rapido")
    price: float = Field(..., ge=0, description="Estimated or booked price")
    currency: str = Field('INR', description="Currency code")
    duration_minutes: int = Field(..., ge=0, description="Estimated duration in minutes")
    eta: Optional[str] = Field(None, description="Estimated arrival time text")
    departure_time: Optional[datetime] = Field(None, description="Scheduled departure time")
    return_trip: Optional[bool] = Field(False, description="Whether includes a return leg")
    status: Literal['pending', 'confirmed', 'cancelled', 'completed'] = Field('confirmed')
    legs: Optional[List[dict]] = Field(default=None, description="Multi-modal legs if applicable")
