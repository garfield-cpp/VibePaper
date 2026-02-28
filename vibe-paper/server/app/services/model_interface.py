from abc import ABC, abstractmethod
from typing import Optional, List, Dict


class BaseAIModel(ABC):
    """AI模型的抽象基类"""
    
    @abstractmethod
    def chat_completion(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1000, tools: Optional[List[Dict]] = None, tool_choice: str = "auto") -> Dict:
        """聊天完成功能"""
        pass
    
    @abstractmethod
    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """生成图片"""
        pass
    
    def get_model_info(self) -> Dict:
        """获取模型信息"""
        return {}


class ModelFactory:
    """模型工厂类，用于创建不同的模型实例"""
    
    @staticmethod
    def create_model(provider: str, model_name: str, api_key: str, **kwargs) -> BaseAIModel:
        """创建模型实例"""
        if provider == "openai":
            from .models.openai_model import OpenAIModel
            return OpenAIModel(model_name, api_key)
        elif provider == "aliyun":
            from .models.aliyun_model import AliyunModel
            return AliyunModel(model_name, api_key, **kwargs)
        elif provider == "volcengine":
            from .models.volcengine_model import VolcengineModel
            return VolcengineModel(model_name, api_key, **kwargs)
        else:
            raise ValueError(f"不支持的模型提供商: {provider}")
