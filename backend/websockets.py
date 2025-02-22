from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
from datetime import datetime
from auth import get_current_user
from models.user import User
from download_manager import download_manager

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def broadcast_to_user(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except WebSocketDisconnect:
                    self.disconnect(connection, user_id)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    try:
        await manager.connect(websocket, user_id)
        while True:
            try:
                # Wait for any message (can be used for ping/pong)
                data = await websocket.receive_text()
                
                # Get current download progress for the user
                downloads = download_manager.get_all_downloads()
                
                # Format and send progress update
                progress_update = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "downloads": [
                        {
                            "filename": d.filename,
                            "total_size": d.total_size,
                            "downloaded": d.downloaded,
                            "speed": d.speed,
                            "status": d.status,
                            "progress": (d.downloaded / d.total_size * 100) if d.total_size > 0 else 0
                        } for d in downloads
                    ]
                }
                
                await manager.broadcast_to_user(progress_update, user_id)
                
            except WebSocketDisconnect:
                manager.disconnect(websocket, user_id)
                break
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket, user_id)

@router.websocket("/ws/download/{download_id}")
async def download_progress_endpoint(websocket: WebSocket, download_id: str):
    try:
        await websocket.accept()
        while True:
            try:
                # Wait for any message
                await websocket.receive_text()
                
                # Get progress for specific download
                progress = download_manager.get_download_progress(download_id)
                if progress:
                    await websocket.send_json({
                        "timestamp": datetime.utcnow().isoformat(),
                        "download": {
                            "filename": progress.filename,
                            "total_size": progress.total_size,
                            "downloaded": progress.downloaded,
                            "speed": progress.speed,
                            "status": progress.status,
                            "progress": (progress.downloaded / progress.total_size * 100) if progress.total_size > 0 else 0
                        }
                    })
            except WebSocketDisconnect:
                break
    except Exception as e:
        print(f"WebSocket error: {str(e)}")