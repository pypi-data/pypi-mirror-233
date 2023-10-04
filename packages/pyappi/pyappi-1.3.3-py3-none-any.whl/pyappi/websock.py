from fastapi import WebSocket
from pyappi.api_base import app


# https://fastapi.tiangolo.com/advanced/websockets/
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")