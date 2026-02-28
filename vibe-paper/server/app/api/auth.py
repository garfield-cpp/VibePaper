from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户"""
    user_id = auth_service.verify_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = auth_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    try:
        user = auth_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    user = auth_service.authenticate_user(user_data)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = auth_service.create_access_token(data={"sub": user.id})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return current_user
