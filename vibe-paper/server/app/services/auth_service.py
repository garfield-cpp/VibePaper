from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
import uuid
import hashlib
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# JWT 配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    def __init__(self):
        # 这里应该是数据库连接，暂时使用内存存储
        self.users = {}
    
    def hash_password(self, password: str) -> str:
        """密码哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """验证密码"""
        return hashlib.sha256(password.encode()).hexdigest() == hashed_password
    
    def create_user(self, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查邮箱是否已存在
        for user in self.users.values():
            if user.email == user_data.email:
                raise ValueError("Email already registered")
        
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            username=user_data.username,
            email=user_data.email,
            password_hash=self.hash_password(user_data.password)
        )
        self.users[user_id] = user
        return user
    
    def authenticate_user(self, user_data: UserLogin) -> Optional[User]:
        """认证用户"""
        # 查找用户
        for user in self.users.values():
            if user.email == user_data.email:
                if self.verify_password(user_data.password, user.password_hash):
                    return user
                break
        return None
    
    def create_access_token(self, data: dict) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[str]:
        """验证令牌"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except JWTError:
            return None
    
    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户"""
        return self.users.get(user_id)
