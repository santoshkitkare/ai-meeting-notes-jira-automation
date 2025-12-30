from fastapi import WebSocket
from typing import Dict

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, job_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[job_id] = websocket

    def disconnect(self, job_id: str):
        self.active_connections.pop(job_id, None)

    async def send_update(self, job_id: str, message: dict):
        ws = self.active_connections.get(job_id)
        if ws:
            await ws.send_json(message)


# ✅ THIS IS THE IMPORTANT PART
ws_manager = WebSocketManager()