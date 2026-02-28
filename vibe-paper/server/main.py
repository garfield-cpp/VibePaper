from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import papers, ai, auth, images

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(papers.router)
app.include_router(ai.router)
app.include_router(images.router)

@app.get("/")
async def root():
    return {"message": "Vibe Paper API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
