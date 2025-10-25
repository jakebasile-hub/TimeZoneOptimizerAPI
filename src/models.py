from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Participant(BaseModel):
    name: str = Field(..., description="Name of the participant")
    location: str = Field(..., description="Location string (e.g., 'New York, USA')")


class OptimizeRequest(BaseModel):
    participants: List[Participant] = Field(..., description="List of meeting participants")
    duration_minutes: int = Field(60, ge=15, le=480, description="Meeting duration in minutes")
    num_alternatives: int = Field(3, ge=1, le=10, description="Number of alternative times to return")


class LocalTime(BaseModel):
    name: str
    local_time: str  # ISO format with timezone


class Alternative(BaseModel):
    utc_time: str  # ISO format UTC
    fairness_score: float = Field(..., ge=0, le=1)


class OptimizeResponse(BaseModel):
    best_meeting_time_utc: str  # ISO format UTC
    local_times: List[LocalTime]
    alternatives: List[Alternative]


class HealthResponse(BaseModel):
    status: str
    uptime: float


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
