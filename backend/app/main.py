from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, WebSocket
from app.db import Base, engine
from app.router import router
from app.websocket_manager import WebSocketManager
# import app.routes.internal as internal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Meeting → Jira")
app.include_router(router)
ws_manager = WebSocketManager()


@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await ws_manager.connect(job_id, websocket)

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except:
        ws_manager.disconnect(job_id)

@app.get("/")
def health():
    return {"status": "running"}
