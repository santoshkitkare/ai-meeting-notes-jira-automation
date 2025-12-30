from fastapi import APIRouter
from app.websocket_manager import ws_manager

router = APIRouter()

@router.post("/internal/notify")
async def notify_client(data: dict):
    import asyncio
    # await ws_manager.send_update(
    #     data["job_id"],
    #     {
    #         "status": data["status"],
    #         "progress": data.get("progress", 0),
    #         "message": data.get("message", ""),
    #         "result": data.get("result")
    #     }
    # )
    asyncio.create_task(
        ws_manager.send_update(
            data["job_id"],
            data
        )
    )

    return {"ok": True}