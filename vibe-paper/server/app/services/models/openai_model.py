import openai
from typing import Optional, List, Dict
from ..model_interface import BaseAIModel


class OpenAIModel(BaseAIModel):
    """OpenAI模型的实现"""
    
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        openai.api_key = api_key
    
    def chat_completion(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1000, tools: Optional[List[Dict]] = None, tool_choice: str = "auto") -> Dict:
        """聊天完成功能"""
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice
        )
        return response
    
    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """生成图片"""
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
        return response['data'][0]['url']
    
    def get_model_info(self) -> Dict:
        """获取模型信息"""
        return {
            "name": self.model_name,
            "provider": "openai"
        }
