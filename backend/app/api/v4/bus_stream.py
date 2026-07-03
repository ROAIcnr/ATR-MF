import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.websockets import WebSocketState
from app.bus.aether_bus import aether_bus
from app.bus.envelopes import AkashicEnvelope
from app.agns.engine import process_intent
from app.core.config import settings

router = APIRouter()

@router.websocket("/stream")
async def bus_stream(ws: WebSocket):
    token = ws.query_params.get("token")
    if not token:
        await ws.close(code=1008, reason="Missing token")
        return

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
        session_id = payload.get("session_id")
        if not session_id:
            await ws.close(code=1008, reason="Missing session_id in token")
            return
    except jwt.PyJWTError as e:
        await ws.close(code=1008, reason="Invalid token")
        return

    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            intent_id = data.get("intent_id", "unknown")
            envelope = AkashicEnvelope.from_payload(
                intent_id=intent_id,
                session_id=session_id,
                payload=data,
            )
            await aether_bus.publish(envelope)

            # simple inline consumer for now
            result = await process_intent(envelope.payload)

            await ws.send_json({
                "intent_id": intent_id,
                "contract": result["contract"],
                "governor_status": result["governor_status"],
                "shannon_entropy": result["shannon_entropy"],
            })
    except WebSocketDisconnect:
        return
