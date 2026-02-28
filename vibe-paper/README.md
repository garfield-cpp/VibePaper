# Vibe Paper - AI 辅助学术论文写作平台

![Vibe Paper](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=A%20modern%20academic%20paper%20writing%20platform%20with%20AI%20assistance%2C%20showing%20a%20collaborative%20editing%20interface%20with%20multiple%20users%20working%20on%20a%20paper%20together%2C%20with%20AI%20suggestions%20and%20version%20control%20features%2C%20professional%20UI%20design%2C%20blue%20and%20white%20color%20scheme&image_size=landscape_16_9)

## 项目介绍

Vibe Paper 是一个结合 AI 技术的学术论文写作辅助工具，旨在帮助用户更高效地进行学术论文的撰写、编辑和管理。通过集成先进的 AI 模型，Vibe Paper 提供了全方位的论文写作辅助功能，包括论文生成、文献搜索、代码仓库搜索、图片生成等。

## 核心功能

### 1. 论文管理系统
- **用户认证**：支持用户注册、登录和权限管理
- **论文操作**：创建、编辑、查看和管理学术论文
- **文件管理**：支持图片上传和管理

### 2. AI 辅助写作功能
- **论文生成**：根据主题和大纲生成学术论文
- **对话式助手**：与 AI 进行实时对话，获取写作建议
- **文献搜索**：通过 AI 搜索相关学术文献
- **代码仓库搜索**：查找相关 GitHub 代码仓库
- **论文大纲生成**：分析论文内容，生成详细章节目录
- **图片生成**：根据提示词生成相关图片
- **论文结构分析**：分析论文结构并提供改进建议
- **审稿模拟**：模拟期刊审稿过程，提供专业评审意见
- **数据可视化**：将数据转换为图表

### 3. 实时协作
- **多人同时编辑**：支持多用户实时协作编辑论文
- **操作同步**：实时同步编辑操作，确保所有用户看到相同的内容
- **光标位置同步**：显示其他用户的光标位置
- **用户状态管理**：显示当前在线用户，通知用户加入和离开

### 4. 版本控制
- **版本历史记录**：自动记录每次编辑的版本
- **版本回滚**：支持回滚到任意历史版本
- **版本信息**：显示版本号、创建时间、创建者等信息

### 5. 多模型支持
- **OpenAI 模型**：GPT-3.5 Turbo、GPT-4、GPT-4o
- **阿里云模型**：通义千问 Plus
- **火山引擎模型**：豆包 Pro

## 技术架构

### 前端
- **框架**：React + TypeScript
- **构建工具**：Vite
- **样式**：TailwindCSS
- **编辑器**：Monaco Editor（代码编辑器）
- **数学公式**：MathJax
- **路由**：React Router

### 后端
- **框架**：FastAPI（Python）
- **数据库**：MongoDB
- **认证**：JWT
- **AI 集成**：OpenAI API、阿里云 API、火山引擎 API
- **实时通信**：WebSocket
- **部署**：支持 Docker 容器化

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MongoDB（可选，默认使用内存存储）

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/yourusername/vibe-paper.git
cd vibe-paper
```

#### 2. 配置环境变量
编辑 `.env` 文件，设置 API 密钥和其他配置：

```env
# 模型提供商配置
MODEL_PROVIDER=openai  # 可选值: openai, aliyun, volcengine
MODEL_NAME=gpt-3.5-turbo  # 具体模型名称

# OpenAI 配置
OPENAI_API_KEY=your-openai-api-key

# 阿里云配置
ALIYUN_API_KEY=your-aliyun-api-key
ALIYUN_API_SECRET=your-aliyun-api-secret
ALIYUN_ENDPOINT=https://ark.cn-beijing.aliyuncs.com/api/v3

# 火山引擎配置
VOLCENGINE_API_KEY=your-volcengine-api-key
VOLCENGINE_ENDPOINT=https://ark.cn-beijing.volces.com/api/v3
```

#### 3. 安装后端依赖
```bash
cd server
pip install -r requirements.txt
```

#### 4. 安装前端依赖
```bash
cd ../client
npm install
```

#### 5. 启动服务器
```bash
# 启动后端服务器
cd ../server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 启动前端服务器（在另一个终端）
cd ../client
npm run dev
```

#### 6. 访问应用
打开浏览器，访问 `http://localhost:5173` 即可使用 Vibe Paper。

## 使用指南

### 1. 创建论文
- 点击首页的「创建论文」按钮
- 输入论文标题和初始内容
- 点击「保存」按钮创建论文

### 2. 编辑论文
- 在编辑器中修改论文内容
- 使用工具栏插入公式和图片
- 点击「保存」按钮保存修改

### 3. 使用 AI 助手
- 在右侧 AI 助手面板中选择模型
- 输入问题或请求
- 点击「发送」按钮获取 AI 回复
- 使用 AI 功能按钮快速执行常用操作

### 4. 实时协作
- 点击「协作管理」按钮添加协作者
- 协作者可以同时编辑论文
- 查看实时显示的在线用户和光标位置

### 5. 版本控制
- 点击「版本管理」按钮查看版本历史
- 选择历史版本查看详细信息
- 点击「回滚到此版本」按钮恢复到指定版本

## 项目结构

```
vibe-paper/
├── client/            # 前端代码
│   ├── src/           # 源代码
│   │   ├── components/  # 组件
│   │   ├── contexts/    # 上下文
│   │   ├── pages/       # 页面
│   │   ├── App.tsx      # 应用入口
│   │   └── main.tsx     # 主入口
│   ├── public/        # 静态资源
│   ├── package.json   # 依赖配置
│   └── vite.config.ts # Vite 配置
├── server/            # 后端代码
│   ├── app/           # 应用代码
│   │   ├── api/        # API 路由
│   │   ├── models/     # 数据模型
│   │   ├── schemas/    # 数据验证
│   │   └── services/   # 业务逻辑
│   ├── uploads/        # 上传文件
│   ├── main.py         # 应用入口
│   └── requirements.txt # 依赖配置
├── .env               # 环境变量
├── docker-compose.yml # Docker 配置
└── README.md          # 项目说明
```

## 技术亮点

1. **多模型支持**：灵活切换不同的 AI 模型提供商
2. **实时协作**：基于 WebSocket 的实时编辑和光标同步
3. **版本控制**：完整的版本历史记录和回滚功能
4. **功能丰富**：提供全方位的学术论文写作辅助功能
5. **用户友好**：直观的用户界面和流畅的交互体验
6. **可扩展性**：模块化设计，易于添加新功能
7. **安全性**：完善的用户认证和权限管理

## 未来规划

- [ ] 支持更多 AI 模型提供商
- [ ] 实现论文导出为 PDF、Word、LaTeX 等格式
- [ ] 添加更多专业领域的 AI 模型
- [ ] 开发移动应用版本
- [ ] 构建用户社区，分享写作经验和技巧

## 贡献指南

欢迎贡献代码、报告问题或提出建议！请按照以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

- 项目地址：https://github.com/yourusername/vibe-paper
- 问题反馈：https://github.com/yourusername/vibe-paper/issues

---

感谢使用 Vibe Paper！希望它能帮助您更高效地完成学术论文写作。
