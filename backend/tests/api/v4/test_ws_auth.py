import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.v4.bus_stream import router
from app.core.config import settings
import jwt
from starlette.websockets import WebSocketDisconnect

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_ws_no_token():
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with client.websocket_connect("/stream"):
            pass
    assert excinfo.value.code == 1008
    assert excinfo.value.reason == "Missing token"

def test_ws_invalid_token():
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with client.websocket_connect("/stream?token=invalid"):
            pass
    assert excinfo.value.code == 1008
    assert excinfo.value.reason == "Invalid token"

def test_ws_missing_session_id():
    token = jwt.encode(
        {"aud": settings.jwt_audience, "iss": settings.jwt_issuer},
        settings.jwt_secret,
        algorithm="HS256"
    )
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with client.websocket_connect(f"/stream?token={token}"):
            pass
    assert excinfo.value.code == 1008
    assert excinfo.value.reason == "Missing session_id in token"

def test_ws_valid_token():
    token = jwt.encode(
        {"session_id": "test-session", "aud": settings.jwt_audience, "iss": settings.jwt_issuer},
        settings.jwt_secret,
        algorithm="HS256"
    )
    with client.websocket_connect(f"/stream?token={token}") as websocket:
        websocket.send_json({"intent_id": "test"})
        data = websocket.receive_json()
        assert data["intent_id"] == "test"
