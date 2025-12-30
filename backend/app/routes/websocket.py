from fastapi import WebSocket, APIRouter
from app.websocket_manager import ws_manager

router = APIRouter()

@router.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await ws_manager.connect(job_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        ws_manager.disconnect(job_id)
