from typing import Dict, List, Set
from fastapi import WebSocket
import json
import uuid

class ConnectionManager:
    def __init__(self):
        # 存储活动的连接，格式：{paper_id: {user_id: WebSocket}}
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, paper_id: str, user_id: str):
        await websocket.accept()
        if paper_id not in self.active_connections:
            self.active_connections[paper_id] = {}
        self.active_connections[paper_id][user_id] = websocket
        
        # 广播用户加入消息
        await self.broadcast(paper_id, {
            "type": "user_joined",
            "user_id": user_id,
            "message": f"用户 {user_id} 加入了编辑"
        }, exclude_user=user_id)
    
    def disconnect(self, paper_id: str, user_id: str):
        if paper_id in self.active_connections and user_id in self.active_connections[paper_id]:
            del self.active_connections[paper_id][user_id]
            if not self.active_connections[paper_id]:
                del self.active_connections[paper_id]
    
    async def broadcast(self, paper_id: str, message: dict, exclude_user: str = None):
        if paper_id in self.active_connections:
            for user_id, connection in self.active_connections[paper_id].items():
                if user_id != exclude_user:
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        print(f"发送消息失败: {e}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"发送个人消息失败: {e}")
    
    def get_active_users(self, paper_id: str) -> List[str]:
        if paper_id in self.active_connections:
            return list(self.active_connections[paper_id].keys())
        return []

# 创建全局连接管理器
manager = ConnectionManager()
