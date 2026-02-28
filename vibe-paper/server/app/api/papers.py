from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from app.schemas.paper import PaperCreate, PaperUpdate, PaperResponse, CollaboratorRequest, VersionResponse
from app.services.paper_service import PaperService
from app.api.auth import get_current_user
from app.services.websocket_manager import manager
import json
import uuid

router = APIRouter(prefix="/papers", tags=["papers"])
paper_service = PaperService()

@router.post("/", response_model=PaperResponse)
async def create_paper(paper: PaperCreate, current_user = Depends(get_current_user)):
    return paper_service.create_paper(paper, current_user.id)

@router.get("/", response_model=list[PaperResponse])
async def get_papers(current_user = Depends(get_current_user)):
    return paper_service.get_papers(current_user.id)

@router.get("/{paper_id}", response_model=PaperResponse)
async def get_paper(paper_id: str, current_user = Depends(get_current_user)):
    paper = paper_service.get_paper(paper_id, current_user.id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@router.put("/{paper_id}", response_model=PaperResponse)
async def update_paper(paper_id: str, paper: PaperUpdate, current_user = Depends(get_current_user)):
    updated_paper = paper_service.update_paper(paper_id, paper, current_user.id)
    if not updated_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return updated_paper

@router.delete("/{paper_id}")
async def delete_paper(paper_id: str, current_user = Depends(get_current_user)):
    result = paper_service.delete_paper(paper_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Paper not found")
    return {"message": "Paper deleted successfully"}

@router.post("/{paper_id}/collaborators")
async def add_collaborator(paper_id: str, request: CollaboratorRequest, current_user = Depends(get_current_user)):
    paper = paper_service.get_paper(paper_id, current_user.id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # 检查当前用户是否是论文的所有者
    if paper.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the paper owner can add collaborators")
    
    # 添加协作者
    if request.collaborator_id not in paper.collaborators:
        paper.collaborators.append(request.collaborator_id)
        paper_service.papers[paper_id] = paper
    
    return {"message": "Collaborator added successfully", "collaborators": paper.collaborators}

@router.delete("/{paper_id}/collaborators/{collaborator_id}")
async def remove_collaborator(paper_id: str, collaborator_id: str, current_user = Depends(get_current_user)):
    paper = paper_service.get_paper(paper_id, current_user.id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # 检查当前用户是否是论文的所有者
    if paper.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the paper owner can remove collaborators")
    
    # 移除协作者
    if collaborator_id in paper.collaborators:
        paper.collaborators.remove(collaborator_id)
        paper_service.papers[paper_id] = paper
    
    return {"message": "Collaborator removed successfully", "collaborators": paper.collaborators}

@router.get("/{paper_id}/versions", response_model=list[VersionResponse])
async def get_versions(paper_id: str, current_user = Depends(get_current_user)):
    versions = paper_service.get_versions(paper_id, current_user.id)
    if not versions:
        raise HTTPException(status_code=404, detail="No versions found for this paper")
    return versions

@router.get("/{paper_id}/versions/{version_id}", response_model=VersionResponse)
async def get_version(paper_id: str, version_id: str, current_user = Depends(get_current_user)):
    version = paper_service.get_version(paper_id, version_id, current_user.id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version

@router.post("/{paper_id}/versions/{version_id}/rollback", response_model=PaperResponse)
async def rollback_to_version(paper_id: str, version_id: str, current_user = Depends(get_current_user)):
    paper = paper_service.rollback_to_version(paper_id, version_id, current_user.id)
    if not paper:
        raise HTTPException(status_code=404, detail="Failed to rollback to version")
    return paper

@router.websocket("/{paper_id}/ws")
async def websocket_endpoint(websocket: WebSocket, paper_id: str):
    # 从WebSocket连接中获取用户信息
    # 注意：在实际生产环境中，应该通过token验证用户身份
    user_id = websocket.query_params.get("user_id")
    if not user_id:
        await websocket.close(code=1008, reason="Missing user_id")
        return
    
    # 验证用户是否有权限编辑该论文
    # 这里需要添加权限验证逻辑
    
    await manager.connect(websocket, paper_id, user_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            # 处理接收到的编辑操作
            operation_type = data.get("type")
            
            if operation_type == "edit":
                # 广播编辑操作给其他用户
                await manager.broadcast(paper_id, {
                    "type": "edit",
                    "user_id": user_id,
                    "position": data.get("position"),
                    "content": data.get("content"),
                    "operation": data.get("operation")
                }, exclude_user=user_id)
            elif operation_type == "cursor_move":
                # 广播光标位置给其他用户
                await manager.broadcast(paper_id, {
                    "type": "cursor_move",
                    "user_id": user_id,
                    "position": data.get("position")
                }, exclude_user=user_id)
    except WebSocketDisconnect:
        manager.disconnect(paper_id, user_id)
        # 广播用户离开消息
        await manager.broadcast(paper_id, {
            "type": "user_left",
            "user_id": user_id,
            "message": f"用户 {user_id} 离开了编辑"
        })
