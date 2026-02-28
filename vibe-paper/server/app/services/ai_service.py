from typing import Optional, List, Dict
from dotenv import load_dotenv
import os
import json
from .model_interface import ModelFactory

# 加载环境变量
load_dotenv()

# 获取模型配置
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
API_KEY = os.getenv(f"{MODEL_PROVIDER.upper()}_API_KEY", "your-api-key")
API_SECRET = os.getenv(f"{MODEL_PROVIDER.upper()}_API_SECRET", "")
ENDPOINT = os.getenv(f"{MODEL_PROVIDER.upper()}_ENDPOINT", "")

class AIService:
    def __init__(self):
        # 模型配置
        self.models = {
            "gpt-3.5-turbo": {
                "name": "GPT-3.5 Turbo",
                "description": "通用型模型，适合大多数任务",
                "supports_deep_thinking": False
            },
            "gpt-4": {
                "name": "GPT-4",
                "description": "更强大的模型，适合复杂任务",
                "supports_deep_thinking": True
            },
            "gpt-4o": {
                "name": "GPT-4o",
                "description": "最新的多模态模型",
                "supports_deep_thinking": True
            },
            "qwen-plus": {
                "name": "通义千问 Plus",
                "description": "阿里云通义千问大模型",
                "supports_deep_thinking": True
            },
            "doubao-pro": {
                "name": "豆包 Pro",
                "description": "火山引擎豆包大模型",
                "supports_deep_thinking": True
            }
        }
        self.default_model = MODEL_NAME
        
        # 创建模型实例
        model_kwargs = {}
        if API_SECRET:
            model_kwargs["api_secret"] = API_SECRET
        if ENDPOINT:
            model_kwargs["endpoint"] = ENDPOINT
        
        self.model = ModelFactory.create_model(MODEL_PROVIDER, self.default_model, API_KEY, **model_kwargs)
        
        # 函数描述，用于 Function Calling
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_literature",
                    "description": "搜索学术文献，获取相关论文信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜索关键词，例如：'深度学习 图像识别'"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_github",
                    "description": "搜索 GitHub 代码仓库，获取相关项目信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜索关键词，例如：'machine learning library'"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_paper_outline",
                    "description": "分析论文内容，生成详细的章节目录",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "论文内容，需要分析的文本"
                            }
                        },
                        "required": ["content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_image",
                    "description": "生成图片，根据提示词创建图像",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "图片生成提示词，例如：'A beautiful sunset over mountains'"
                            }
                        },
                        "required": ["prompt"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_paper_structure",
                    "description": "分析论文结构，提供改进建议",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "论文内容，需要分析的文本"
                            }
                        },
                        "required": ["content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "simulate_review",
                    "description": "模拟期刊审稿过程，提供改进建议",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "论文内容，需要评审的文本"
                            }
                        },
                        "required": ["content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_visualization",
                    "description": "支持将数据转换为图表",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "string",
                                "description": "需要可视化的数据，例如：'月份,销售额\n1月,1000\n2月,1500\n3月,2000'"
                            },
                            "chart_type": {
                                "type": "string",
                                "description": "图表类型，例如：'柱状图'、'折线图'、'饼图'"
                            }
                        },
                        "required": ["data", "chart_type"]
                    }
                }
            }
        ]
    
    def get_models(self) -> Dict[str, Dict]:
        """获取可用的模型列表"""
        return self.models
    
    def generate_paper(self, topic: str, outline: Optional[str] = None, length: int = 1000, model: str = None, deep_thinking: bool = False) -> str:
        # 使用指定模型或默认模型
        model = model or self.default_model
        
        prompt = f"请生成一篇关于 '{topic}' 的学术论文"
        if outline:
            prompt += f"，大纲如下：\n{outline}"
        prompt += f"\n论文长度约 {length} 字，要求结构清晰，逻辑严谨，符合学术规范。"
        
        # 如果启用深度思考且模型支持
        if deep_thinking and self.models[model].get("supports_deep_thinking", False):
            prompt = "请深度思考这个问题，然后提供详细的回答。\n" + prompt
        
        messages = [
            {"role": "system", "content": "你是一位专业的学术论文撰写助手，擅长生成高质量的学术论文。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.model.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=int(length * 1.5)  # 预留一些额外的 tokens
        )
        
        return response['choices'][0]['message']['content']
    
    def conversation(self, message: str, context: Optional[List[str]] = None, model: str = None, deep_thinking: bool = False) -> str:
        # 使用指定模型或默认模型
        model = model or self.default_model
        
        # 构建对话历史
        messages = [
            {"role": "system", "content": "你是一位专业的学术论文撰写助手，擅长与用户交流并提供学术建议。当需要查询信息或执行特定任务时，请使用提供的工具。"}
        ]
        
        # 添加上下文
        if context:
            for i, msg in enumerate(context):
                role = "user" if i % 2 == 0 else "assistant"
                messages.append({"role": role, "content": msg})
        
        # 添加当前消息
        user_message = message
        # 如果启用深度思考且模型支持
        if deep_thinking and self.models[model].get("supports_deep_thinking", False):
            user_message = "请深度思考这个问题，然后提供详细的回答。\n" + user_message
        messages.append({"role": "user", "content": user_message})
        
        # 第一次调用模型，可能会返回函数调用请求
        response = self.model.chat_completion(
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=1000
        )
        
        response_message = response['choices'][0]['message']
        
        # 检查是否需要调用函数
        if 'tool_calls' in response_message:
            # 处理函数调用
            for tool_call in response_message['tool_calls']:
                function_name = tool_call['function']['name']
                function_args = json.loads(tool_call['function']['arguments'])
                
                # 执行函数
                tool_result = self._execute_function(function_name, function_args)
                
                # 添加函数调用结果到对话历史
                messages.append(response_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call['id'],
                    "name": function_name,
                    "content": tool_result
                })
            
            # 再次调用模型，获取最终回复
            second_response = self.model.chat_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return second_response['choices'][0]['message']['content']
        else:
            # 直接返回模型回复
            return response_message['content']
    
    def _execute_function(self, function_name: str, function_args: dict) -> str:
        """执行函数调用"""
        if function_name == "search_literature":
            return self.search_literature(function_args.get("query"))
        elif function_name == "search_github":
            return self.search_github(function_args.get("query"))
        elif function_name == "get_paper_outline":
            return self.get_paper_outline(function_args.get("content"))
        elif function_name == "generate_image":
            return self.generate_image(function_args.get("prompt"))
        elif function_name == "analyze_paper_structure":
            return self.analyze_paper_structure(function_args.get("content"))
        elif function_name == "simulate_review":
            return self.simulate_review(function_args.get("content"))
        elif function_name == "generate_visualization":
            return self.generate_visualization(function_args.get("data"), function_args.get("chart_type"))
        else:
            return f"未知函数: {function_name}"
    
    def search_literature(self, query: str, model: str = None) -> str:
        """搜索文献"""
        # 使用指定模型或默认模型
        model = model or self.default_model
        
        prompt = f"请搜索关于 '{query}' 的相关学术文献，并提供以下信息：\n1. 文献标题\n2. 作者\n3. 发表年份\n4. 期刊/会议\n5. 摘要\n6. 链接（如果有）\n\n请至少提供5篇相关文献。"
        
        messages = [
            {"role": "system", "content": "你是一位专业的学术文献搜索助手，擅长查找和整理相关学术文献。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.model.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        return response['choices'][0]['message']['content']
    
    def search_github(self, query: str, model: str = None) -> str:
        """搜索 GitHub 代码仓库"""
        # 使用指定模型或默认模型
        model = model or self.default_model
        
        prompt = f"请搜索关于 '{query}' 的相关 GitHub 代码仓库，并提供以下信息：\n1. 仓库名称\n2. 描述\n3. 星标数\n4. 主要语言\n5. 链接\n\n请至少提供5个相关仓库。"
        
        messages = [
            {"role": "system", "content": "你是一位专业的 GitHub 代码仓库搜索助手，擅长查找和整理相关代码仓库。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.model.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        return response['choices'][0]['message']['content']
    
    def get_paper_outline(self, content: str, model: str = None) -> str:
        """获取文章的章节目录"""
        # 使用指定模型或默认模型
        model = model or self.default_model
        
        prompt = f"请分析以下论文内容，并生成一个详细的章节目录：\n\n{content}\n\n章节目录应该包括：\n1. 主要章节标题\n2. 子章节标题（如果有）\n3. 每个章节的简要描述\n\n请以结构化的方式呈现。"
        
        messages = [
            {"role": "system", "content": "你是一位专业的论文分析助手，擅长提取和整理论文的结构。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.model.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response['choices'][0]['message']['content']
    
    def generate_image(self, prompt: str, model: str = None) -> str:
        """生成图片"""
        # 使用指定模型或默认模型
        model = model or self.default_model
        
        try:
            # 使用模型实例生成图片
            image_url = self.model.generate_image(prompt, size="1024x1024")
            return image_url
        except Exception as e:
            # 如果调用失败，返回错误信息
            return f"图片生成失败：{str(e)}"
    
    def analyze_paper_structure(self, content: str, model: str = None) -> str:
        """分析论文结构，提供改进建议"""
        # 使用指定模型或默认模型
        model = model or self.default_model
        
        prompt = f"请分析以下论文内容的结构，并提供详细的改进建议：\n\n{content}\n\n分析应该包括：\n1. 论文结构的优点\n2. 论文结构的缺点\n3. 具体的改进建议\n4. 结构优化的具体步骤\n\n请以结构化的方式呈现分析结果。" 
        
        messages = [
            {"role": "system", "content": "你是一位专业的论文结构分析专家，擅长分析学术论文的结构并提供改进建议。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.model.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        return response['choices'][0]['message']['content']
    
    def simulate_review(self, content: str, model: str = None) -> str:
        """模拟期刊审稿过程，提供改进建议"""
        # 使用指定模型或默认模型
        model = model or self.default_model
        
        prompt = f"请模拟期刊审稿过程，对以下论文内容进行评审，并提供详细的改进建议：\n\n{content}\n\n评审应该包括：\n1. 论文的 strengths（优点）\n2. 论文的 weaknesses（缺点）\n3. 具体的改进建议\n4. 评审结论（例如：接受、修改后接受、拒绝）\n\n请以专业的审稿人语气呈现评审结果。" 
        
        messages = [
            {"role": "system", "content": "你是一位专业的学术期刊审稿人，擅长评审学术论文并提供详细的改进建议。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.model.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        return response['choices'][0]['message']['content']
    
    def generate_visualization(self, data: str, chart_type: str, model: str = None) -> str:
        """支持将数据转换为图表"""
        # 使用指定模型或默认模型
        model = model or self.default_model
        
        prompt = f"请根据以下数据生成一个{chart_type}图表，并提供详细的图表描述：\n\n数据：{data}\n\n图表应该包括：\n1. 图表标题\n2. 坐标轴标签\n3. 数据系列\n4. 图例（如果需要）\n\n请提供图表的详细描述和生成建议。" 
        
        messages = [
            {"role": "system", "content": "你是一位专业的数据可视化专家，擅长根据数据生成合适的图表并提供详细描述。"},
            {"role": "user", "content": prompt}
        ]
        
        response = self.model.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        return response['choices'][0]['message']['content']
