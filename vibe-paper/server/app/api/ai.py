from fastapi import APIRouter, HTTPException
from app.schemas.ai import (
    AIGenerateRequest, AIGenerateResponse, 
    AIConversationRequest, AIConversationResponse,
    AISearchRequest, AISearchResponse,
    AIPaperOutlineRequest, AIPaperOutlineResponse,
    AIGenerateImageRequest, AIGenerateImageResponse
)
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])
ai_service = AIService()

@router.get("/models")
async def get_models():
    try:
        return ai_service.get_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate", response_model=AIGenerateResponse)
async def generate_paper(request: AIGenerateRequest):
    try:
        result = ai_service.generate_paper(
            request.topic, 
            request.outline, 
            request.length,
            request.model,
            request.deep_thinking
        )
        return AIGenerateResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation", response_model=AIConversationResponse)
async def conversation(request: AIConversationRequest):
    try:
        result = ai_service.conversation(
            request.message, 
            request.context,
            request.model,
            request.deep_thinking
        )
        return AIConversationResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search/literature", response_model=AISearchResponse)
async def search_literature(request: AISearchRequest):
    try:
        result = ai_service.search_literature(
            request.query,
            request.model
        )
        return AISearchResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search/github", response_model=AISearchResponse)
async def search_github(request: AISearchRequest):
    try:
        result = ai_service.search_github(
            request.query,
            request.model
        )
        return AISearchResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/paper/outline", response_model=AIPaperOutlineResponse)
async def get_paper_outline(request: AIPaperOutlineRequest):
    try:
        result = ai_service.get_paper_outline(
            request.content,
            request.model
        )
        return AIPaperOutlineResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/image/generate", response_model=AIGenerateImageResponse)
async def generate_image(request: AIGenerateImageRequest):
    try:
        result = ai_service.generate_image(
            request.prompt,
            request.model
        )
        return AIGenerateImageResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
