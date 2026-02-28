import json
import requests
from typing import Optional, List, Dict
from ..model_interface import BaseAIModel


class AliyunModel(BaseAIModel):
    """阿里云模型的实现"""
    
    def __init__(self, model_name: str, api_key: str, api_secret: str, endpoint: str = "https://ark.cn-beijing.aliyuncs.com/api/v3"):
        self.model_name = model_name
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = endpoint
    
    def chat_completion(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1000, tools: Optional[List[Dict]] = None, tool_choice: str = "auto") -> Dict:
        """聊天完成功能"""
        # 构建请求数据
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # 处理工具调用
        if tools:
            data["tools"] = tools
            data["tool_choice"] = tool_choice
        
        # 发送请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(
            f"{self.endpoint}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"阿里云API调用失败: {response.text}")
        
        return response.json()
    
    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """生成图片"""
        # 构建请求数据
        data = {
            "prompt": prompt,
            "size": size,
            "n": 1
        }
        
        # 发送请求
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post(
            f"{self.endpoint}/images/generations",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"阿里云图片生成失败: {response.text}")
        
        result = response.json()
        return result['data'][0]['url']
    
    def get_model_info(self) -> Dict:
        """获取模型信息"""
        return {
            "name": self.model_name,
            "provider": "aliyun",
            "endpoint": self.endpoint
        }
