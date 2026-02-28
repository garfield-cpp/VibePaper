from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from app.api.auth import get_current_user
import os
import uuid
from datetime import datetime

router = APIRouter(prefix="/images", tags=["images"])

# 确保上传目录存在
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    paper_id: str = None,
    current_user = Depends(get_current_user)
):
    try:
        # 生成唯一的文件名
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # 创建用户和论文的目录结构
        user_dir = os.path.join(UPLOAD_DIR, current_user.id)
        paper_dir = os.path.join(user_dir, paper_id) if paper_id else user_dir
        os.makedirs(paper_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(paper_dir, unique_filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 生成访问 URL
        image_url = f"/images/{current_user.id}/{paper_id}/{unique_filename}" if paper_id else f"/images/{current_user.id}/{unique_filename}"
        
        return JSONResponse(
            status_code=200,
            content={"message": "Image uploaded successfully", "url": image_url}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/{paper_id}/{filename}")
async def get_image(user_id: str, paper_id: str, filename: str, current_user = Depends(get_current_user)):
    # 确保用户只能访问自己的图片
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    file_path = os.path.join(UPLOAD_DIR, user_id, paper_id, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path)

@router.get("/{user_id}/{filename}")
async def get_image_no_paper(user_id: str, filename: str, current_user = Depends(get_current_user)):
    # 确保用户只能访问自己的图片
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    file_path = os.path.join(UPLOAD_DIR, user_id, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path)
