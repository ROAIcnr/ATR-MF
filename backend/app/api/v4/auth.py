from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HandshakeRequest(BaseModel):
    device_fingerprint: str
    client_capabilities: dict

class HandshakeResponse(BaseModel):
    access_token: str
    session_id: str

@router.post("/handshake", response_model=HandshakeResponse)
async def handshake(body: HandshakeRequest):
    # TODO: generate JWT, store Client_Session
    return HandshakeResponse(
        access_token="demo-token",
        session_id="session-demo",
    )
