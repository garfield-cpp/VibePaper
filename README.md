# Vibe Paper - AI-Assisted Academic Paper Writing Platform

![Vibe Paper](figures/vibe_paper_fig.png)

## Project Introduction

Vibe Paper is an AI-assisted academic paper writing tool designed to help users more efficiently compose, edit, and manage academic papers. By integrating advanced AI models, Vibe Paper provides comprehensive paper writing assistance features, including paper generation, literature search, code repository search, image generation, and more.

## Core Features

### 1. Paper Management System
- **User Authentication**: Supports user registration, login, and permission management
- **Paper Operations**: Create, edit, view, and manage academic papers
- **File Management**: Supports image upload and management

### 2. AI-Assisted Writing Features
- **Paper Generation**: Generate academic papers based on topics and outlines
- **Conversational Assistant**: Have real-time conversations with AI to get writing suggestions
- **Literature Search**: Search for relevant academic literature through AI
- **GitHub Repository Search**: Find relevant GitHub code repositories
- **Paper Outline Generation**: Analyze paper content and generate detailed chapter outlines
- **Image Generation**: Generate relevant images based on prompts
- **Paper Structure Analysis**: Analyze paper structure and provide improvement suggestions
- **Review Simulation**: Simulate journal review process and provide professional review comments
- **Data Visualization**: Convert data into charts

### 3. Real-time Collaboration
- **Multi-user Simultaneous Editing**: Supports multiple users editing papers simultaneously
- **Operation Synchronization**: Real-time synchronization of editing operations to ensure all users see the same content
- **Cursor Position Synchronization**: Display other users' cursor positions
- **User Status Management**: Show current online users, notify users of join and leave events

### 4. Version Control
- **Version History Recording**: Automatically record versions of each edit
- **Version Rollback**: Support rollback to any historical version
- **Version Information**: Display version number, creation time, creator, and other information

### 5. Multi-model Support
- **OpenAI Models**: GPT-3.5 Turbo, GPT-4, GPT-4o
- **Alibaba Cloud Models**: Tongyi Qianwen Plus
- **Volcengine Models**: Doubao Pro

## Technical Architecture

### Frontend
- **Framework**: React + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **Editor**: Monaco Editor (code editor)
- **Math Formulas**: MathJax
- **Routing**: React Router

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **Authentication**: JWT
- **AI Integration**: OpenAI API, Alibaba Cloud API, Volcengine API
- **Real-time Communication**: WebSocket
- **Deployment**: Docker containerization support

## Quick Start

### Environment Requirements
- Python 3.8+
- Node.js 16+
- MongoDB (optional, memory storage used by default)

### Installation Steps

#### 1. Clone the Project
```bash
git clone https://github.com/yourusername/vibe-paper.git
cd vibe-paper
```

#### 2. Configure Environment Variables
Edit the `.env` file and set API keys and other configurations:

```env
# Model provider configuration
MODEL_PROVIDER=openai  # Optional values: openai, aliyun, volcengine
MODEL_NAME=gpt-3.5-turbo  # Specific model name

# OpenAI configuration
OPENAI_API_KEY=your-openai-api-key

# Alibaba Cloud configuration
ALIYUN_API_KEY=your-aliyun-api-key
ALIYUN_API_SECRET=your-aliyun-api-secret
ALIYUN_ENDPOINT=https://ark.cn-beijing.aliyuncs.com/api/v3

# Volcengine configuration
VOLCENGINE_API_KEY=your-volcengine-api-key
VOLCENGINE_ENDPOINT=https://ark.cn-beijing.volces.com/api/v3
```

#### 3. Install Backend Dependencies
```bash
cd server
pip install -r requirements.txt
```

#### 4. Install Frontend Dependencies
```bash
cd ../client
npm install
```

#### 5. Start the Servers
```bash
# Start backend server
cd ../server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start frontend server (in another terminal)
cd ../client
npm run dev
```

#### 6. Access the Application
Open your browser and visit `http://localhost:5173` to use Vibe Paper.

## Usage Guide

### 1. Create a Paper
- Click the "Create Paper" button on the homepage
- Enter the paper title and initial content
- Click the "Save" button to create the paper

### 2. Edit a Paper
- Modify the paper content in the editor
- Use the toolbar to insert formulas and images
- Click the "Save" button to save changes

### 3. Use AI Assistant
- Select a model in the AI Assistant panel on the right
- Enter questions or requests
- Click the "Send" button to get AI responses
- Use AI function buttons to quickly perform common operations

### 4. Real-time Collaboration
- Click the "Collaboration Management" button to add collaborators
- Collaborators can edit the paper simultaneously
- View real-time display of online users and cursor positions

### 5. Version Control
- Click the "Version Management" button to view version history
- Select historical versions to view details
- Click the "Rollback to this version" button to restore to the specified version

## Project Structure

```
vibe-paper/
├── client/            # Frontend code
│   ├── src/           # Source code
│   │   ├── components/  # Components
│   │   ├── contexts/    # Contexts
│   │   ├── pages/       # Pages
│   │   ├── App.tsx      # Application entry
│   │   └── main.tsx     # Main entry
│   ├── public/        # Static resources
│   ├── package.json   # Dependency configuration
│   └── vite.config.ts # Vite configuration
├── server/            # Backend code
│   ├── app/           # Application code
│   │   ├── api/        # API routes
│   │   ├── models/     # Data models
│   │   ├── schemas/    # Data validation
│   │   └── services/   # Business logic
│   ├── uploads/        # Uploaded files
│   ├── main.py         # Application entry
│   └── requirements.txt # Dependency configuration
├── .env               # Environment variables
├── docker-compose.yml # Docker configuration
└── README.md          # Project documentation
```

## Technical Highlights

1. **Multi-model Support**: Flexible switching between different AI model providers
2. **Real-time Collaboration**: WebSocket-based real-time editing and cursor synchronization
3. **Version Control**: Complete version history recording and rollback functionality
4. **Rich Features**: Provides comprehensive academic paper writing assistance features
5. **User-friendly**: Intuitive user interface and smooth interaction experience
6. **Extensibility**: Modular design, easy to add new features
7. **Security**: Comprehensive user authentication and permission management

## Future Plans

- [ ] Support more AI model providers
- [ ] Implement paper export to PDF, Word, LaTeX, and other formats
- [ ] Add more domain-specific AI models
- [ ] Develop mobile application version
- [ ] Build user community to share writing experiences and tips

## Contribution Guide

Welcome to contribute code, report issues, or suggest improvements! Please follow these steps:

1. Fork this project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

- Project Address: https://github.com/yourusername/vibe-paper
- Issue Feedback: https://github.com/yourusername/vibe-paper/issues

---

Thank you for using Vibe Paper! We hope it helps you complete your academic paper writing more efficiently.
