from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()

class TelemetryPulse(BaseModel):
    fps_average: float
    thermal_throttling_status: bool
    memory_pressure: float

@router.put("/pulse", status_code=status.HTTP_204_NO_CONTENT)
async def telemetry_pulse(body: TelemetryPulse):
    # TODO: publish to Kafka / TSDB, feed Governor adaptive throttling
    return
