from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from app.agns.engine import process_intent

router = APIRouter()

class CognitionRequest(BaseModel):
    context_vector: str
    emotional_valence: float
    energy_level: float

class IRResponse(BaseModel):
    ir: Dict[str, Any]
    governor_status: str
    shannon_entropy: float

@router.post("/manifest", response_model=IRResponse)
async def manifest(body: CognitionRequest):
    payload = {
        "state": "THINKING",
        "confidence": 0.8,
        "energy_level": body.energy_level,
        "context_vector": body.context_vector,
        "emotional_valence": body.emotional_valence,
    }
    ir = await process_intent(payload)
    return IRResponse(**ir)
