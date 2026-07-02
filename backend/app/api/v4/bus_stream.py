from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.bus.aether_bus import aether_bus
from app.bus.envelopes import AkashicEnvelope
from app.agns.engine import process_intent

router = APIRouter()

@router.websocket("/stream")
async def bus_stream(ws: WebSocket):
    await ws.accept()
    session_id = "session-ws-demo"  # TODO: derive from JWT/query
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
            ir = await process_intent(envelope.payload)

            await ws.send_json({
                "intent_id": intent_id,
                "ir": ir["ir"],
                "governor_status": ir["governor_status"],
                "shannon_entropy": ir["shannon_entropy"],
            })
    except WebSocketDisconnect:
        return
