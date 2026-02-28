import { useState, useRef, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const PaperEditor = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [saving, setSaving] = useState(false);
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([]);
  const [aiInput, setAiInput] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [models, setModels] = useState<{ [key: string]: { name: string; description: string; supports_deep_thinking: boolean } }>({});
  const [selectedModel, setSelectedModel] = useState('gpt-3.5-turbo');
  const [deepThinking, setDeepThinking] = useState(false);
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);
  const [activeUsers, setActiveUsers] = useState<string[]>([]);
  const [cursorPositions, setCursorPositions] = useState<{ [userId: string]: number }>({});
  const [versions, setVersions] = useState<any[]>([]);
  const [showVersions, setShowVersions] = useState(false);
  const [loadingVersions, setLoadingVersions] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { token, user } = useAuth();
  const editorRef = useRef<any>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // 获取模型列表
    const fetchModels = async () => {
      try {
        const response = await fetch('http://localhost:8000/ai/models');
        if (response.ok) {
          const data = await response.json();
          setModels(data);
        }
      } catch (error) {
        console.error('获取模型列表失败:', error);
      }
    };

    fetchModels();
  }, []);

  useEffect(() => {
    // 建立WebSocket连接
    if (id && user) {
      const ws = new WebSocket(`ws://localhost:8000/papers/${id}/ws?user_id=${user.id}`);
      
      ws.onopen = () => {
        console.log('WebSocket连接已建立');
        setWebsocket(ws);
      };
      
      ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        
        switch (message.type) {
          case 'edit':
            // 处理其他用户的编辑操作
            handleRemoteEdit(message);
            break;
          case 'cursor_move':
            // 处理其他用户的光标移动
            setCursorPositions(prev => ({
              ...prev,
              [message.user_id]: message.position
            }));
            break;
          case 'user_joined':
            // 处理用户加入
            setMessages(prev => [...prev, { role: 'assistant', content: message.message }]);
            break;
          case 'user_left':
            // 处理用户离开
            setMessages(prev => [...prev, { role: 'assistant', content: message.message }]);
            setActiveUsers(prev => prev.filter(userId => userId !== message.user_id));
            setCursorPositions(prev => {
              const newPositions = { ...prev };
              delete newPositions[message.user_id];
              return newPositions;
            });
            break;
        }
      };
      
      ws.onclose = () => {
        console.log('WebSocket连接已关闭');
        setWebsocket(null);
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket错误:', error);
      };
      
      // 组件卸载时关闭连接
      return () => {
        ws.close();
      };
    }
  }, [id, user]);

  // 处理远程编辑操作
  const handleRemoteEdit = (message: any) => {
    // 这里需要实现编辑操作的应用逻辑
    // 例如，根据操作类型（插入、删除、更新）和位置应用变更
    console.log('收到远程编辑操作:', message);
  };

  // 处理本地编辑操作
  const handleLocalEdit = (value: string | undefined) => {
    const newContent = value || '';
    setContent(newContent);
    
    // 发送编辑操作到服务器
    if (websocket && user) {
      websocket.send(JSON.stringify({
        type: 'edit',
        position: 0, // 这里需要获取实际的编辑位置
        content: newContent,
        operation: 'update'
      }));
    }
  };

  // 处理光标移动
  const handleCursorMove = (position: number) => {
    if (websocket && user) {
      websocket.send(JSON.stringify({
        type: 'cursor_move',
        position
      }));
    }
  };

  // 获取版本历史
  const fetchVersions = async () => {
    if (!id || !token) return;
    
    setLoadingVersions(true);
    try {
      const response = await fetch(`http://localhost:8000/papers/${id}/versions`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setVersions(data);
      }
    } catch (error) {
      console.error('获取版本历史失败:', error);
    } finally {
      setLoadingVersions(false);
    }
  };

  // 回滚到指定版本
  const rollbackToVersion = async (versionId: string) => {
    if (!id || !token) return;
    
    try {
      const response = await fetch(`http://localhost:8000/papers/${id}/versions/${versionId}/rollback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const paper = await response.json();
        setTitle(paper.title);
        setContent(paper.content);
        setMessages(prev => [...prev, { role: 'assistant', content: '已成功回滚到选定版本' }]);
        // 重新获取版本历史
        fetchVersions();
      }
    } catch (error) {
      console.error('回滚版本失败:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: '回滚版本失败，请重试' }]);
    }
  };

  // 加载版本历史
  useEffect(() => {
    if (id) {
      fetchVersions();
    }
  }, [id]);

  // 当选择模型改变时，检查是否支持深度思考
  useEffect(() => {
    if (models[selectedModel] && !models[selectedModel].supports_deep_thinking) {
      setDeepThinking(false);
    }
  }, [selectedModel, models]);

  // 加载 MathJax 脚本
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
    script.async = true;
    script.id = 'MathJax-script';
    script.setAttribute('data-config', JSON.stringify({
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']]
      },
      svg: {
        fontCache: 'global'
      }
    }));
    document.head.appendChild(script);
    
    return () => {
      const mathJaxScript = document.getElementById('MathJax-script');
      if (mathJaxScript) {
        document.head.removeChild(mathJaxScript);
      }
    };
  }, []);

  // 当内容改变时，重新渲染 MathJax
  useEffect(() => {
    // 等待 MathJax 加载完成
    setTimeout(() => {
      if (window.MathJax) {
        window.MathJax.typeset();
      }
    }, 100);
  }, [content]);

  // 加载论文内容
  useEffect(() => {
    if (id) {
      const fetchPaper = async () => {
        try {
          const response = await fetch(`http://localhost:8000/papers/${id}`, {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
          if (response.ok) {
            const paper = await response.json();
            setTitle(paper.title);
            setContent(paper.content);
          } else {
            alert('获取论文失败');
            navigate('/papers');
          }
        } catch (error) {
          console.error('Error fetching paper:', error);
          alert('网络错误，请稍后重试');
          navigate('/papers');
        }
      };
      fetchPaper();
    }
  }, [id, token, navigate]);

  const handleSave = async () => {
    setSaving(true);
    try {
      const paperData = {
        title,
        content,
      };

      let response;
      if (id) {
        // 更新现有论文
        response = await fetch(`http://localhost:8000/papers/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(paperData),
        });
      } else {
        // 创建新论文
        response = await fetch('http://localhost:8000/papers', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(paperData),
        });
      }

      if (response.ok) {
        const savedPaper = await response.json();
        if (!id) {
          // 如果是新创建的论文，跳转到编辑页面
          navigate(`/editor/${savedPaper.id}`);
        }
        alert('论文保存成功！');
      } else {
        throw new Error('保存失败');
      }
    } catch (error) {
      console.error('保存失败:', error);
      alert('保存失败，请重试');
    } finally {
      setSaving(false);
    }
  };

  const handleAiSend = async () => {
    if (!aiInput.trim()) return;

    const userMessage = { role: 'user' as const, content: aiInput };
    setMessages(prev => [...prev, userMessage]);
    setAiInput('');
    setAiLoading(true);

    try {
      // 调用后端 API 与 AI 对话
      const response = await fetch('http://localhost:8000/ai/conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: aiInput,
          context: messages.map(msg => msg.content),
          model: selectedModel,
          deep_thinking: deepThinking
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = { role: 'assistant' as const, content: data.content };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('API 调用失败');
      }
    } catch (error) {
      console.error('发送失败:', error);
      // 模拟 AI 回复
      setTimeout(() => {
        const aiMessage = { role: 'assistant' as const, content: `我是 AI 助手，我收到了你的消息：${aiInput}\n\n这里是一些论文写作的建议...` };
        setMessages(prev => [...prev, aiMessage]);
      }, 1000);
    } finally {
      setAiLoading(false);
    }
  };

  const handleAiEdit = () => {
    // 模拟 AI 编辑论文内容
    setContent(prev => prev + '\n\n// AI 编辑的内容：这是 AI 为你添加的内容，用于演示 AI 直接修改论文的功能。');
  };

  const handleAiOutline = () => {
    // 模拟 AI 生成大纲
    const outline = `# 论文大纲\n\n1. 引言\n2. 文献综述\n3. 研究方法\n4. 实验结果\n5. 讨论\n6. 结论\n7. 参考文献`;
    setContent(outline);
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const formData = new FormData();
      formData.append('file', file);
      if (id) {
        formData.append('paper_id', id);
      }

      const response = await fetch('http://localhost:8000/images/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        // 在编辑器中插入图片的 Markdown 语法
        const imageMarkdown = `![图片](${data.url})\n`;
        setContent(prev => prev + imageMarkdown);
      } else {
        throw new Error('图片上传失败');
      }
    } catch (error) {
      console.error('图片上传失败:', error);
      alert('图片上传失败，请重试');
    } finally {
      // 重置文件输入
      e.target.value = '';
    }
  };

  const handleSearchLiterature = async () => {
    const query = prompt('请输入文献搜索关键词：');
    if (!query) return;

    setAiLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ai/search/literature', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          query,
          model: selectedModel
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = { role: 'assistant' as const, content: data.content };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('文献搜索失败');
      }
    } catch (error) {
      console.error('文献搜索失败:', error);
      const aiMessage = { role: 'assistant' as const, content: `文献搜索失败，请重试。` };
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setAiLoading(false);
    }
  };

  const handleSearchGithub = async () => {
    const query = prompt('请输入 GitHub 仓库搜索关键词：');
    if (!query) return;

    setAiLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ai/search/github', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          query,
          model: selectedModel
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = { role: 'assistant' as const, content: data.content };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('GitHub 仓库搜索失败');
      }
    } catch (error) {
      console.error('GitHub 仓库搜索失败:', error);
      const aiMessage = { role: 'assistant' as const, content: `GitHub 仓库搜索失败，请重试。` };
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setAiLoading(false);
    }
  };

  const handleGetPaperOutline = async () => {
    if (!content) {
      alert('请先输入论文内容');
      return;
    }

    setAiLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ai/paper/outline', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          content,
          model: selectedModel
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = { role: 'assistant' as const, content: data.content };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('获取章节目录失败');
      }
    } catch (error) {
      console.error('获取章节目录失败:', error);
      const aiMessage = { role: 'assistant' as const, content: `获取章节目录失败，请重试。` };
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setAiLoading(false);
    }
  };

  const handleGenerateImage = async () => {
    const prompt = prompt('请输入图片生成提示词：');
    if (!prompt) return;

    setAiLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ai/image/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          prompt,
          model: selectedModel
        }),
      });

      if (response.ok) {
        const data = await response.json();
        // 检查返回的是否是图片 URL
        if (data.content.startsWith('http')) {
          // 生成图片成功，将图片 URL 插入到论文中
          const imageMarkdown = `![生成图片](${data.content})\n`;
          setContent(prev => prev + imageMarkdown);
          // 同时在 AI 对话中显示
          const aiMessage = { role: 'assistant' as const, content: `已生成图片并插入到论文中：\n${data.content}` };
          setMessages(prev => [...prev, aiMessage]);
        } else {
          // 生成图片失败
          const aiMessage = { role: 'assistant' as const, content: data.content };
          setMessages(prev => [...prev, aiMessage]);
        }
      } else {
        throw new Error('图片生成失败');
      }
    } catch (error) {
      console.error('图片生成失败:', error);
      const aiMessage = { role: 'assistant' as const, content: `图片生成失败，请重试。` };
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setAiLoading(false);
    }
  };

  const handleAnalyzeStructure = async () => {
    if (!content) {
      alert('请先输入论文内容');
      return;
    }

    setAiLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ai/conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: `请分析以下论文的结构并提供改进建议：\n\n${content}`,
          model: selectedModel,
          deep_thinking: deepThinking
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = { role: 'assistant' as const, content: data.content };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('论文结构分析失败');
      }
    } catch (error) {
      console.error('论文结构分析失败:', error);
      const aiMessage = { role: 'assistant' as const, content: `论文结构分析失败，请重试。` };
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setAiLoading(false);
    }
  };

  const handleSimulateReview = async () => {
    if (!content) {
      alert('请先输入论文内容');
      return;
    }

    setAiLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ai/conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: `请模拟期刊审稿过程，对以下论文进行评审并提供改进建议：\n\n${content}`,
          model: selectedModel,
          deep_thinking: deepThinking
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = { role: 'assistant' as const, content: data.content };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('审稿意见模拟失败');
      }
    } catch (error) {
      console.error('审稿意见模拟失败:', error);
      const aiMessage = { role: 'assistant' as const, content: `审稿意见模拟失败，请重试。` };
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setAiLoading(false);
    }
  };

  const handleGenerateVisualization = async () => {
    const data = prompt('请输入需要可视化的数据（格式：行内用逗号分隔，行之间用换行）：\n例如：\n月份,销售额\n1月,1000\n2月,1500\n3月,2000');
    if (!data) return;

    const chartType = prompt('请选择图表类型：\n1. 柱状图\n2. 折线图\n3. 饼图');
    if (!chartType) return;

    setAiLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ai/conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: `请根据以下数据生成一个${chartType}图表，并提供详细的图表描述：\n\n数据：${data}`,
          model: selectedModel,
          deep_thinking: deepThinking
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const aiMessage = { role: 'assistant' as const, content: data.content };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('数据可视化失败');
      }
    } catch (error) {
      console.error('数据可视化失败:', error);
      const aiMessage = { role: 'assistant' as const, content: `数据可视化失败，请重试。` };
      setMessages(prev => [...prev, aiMessage]);
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <Link to="/" className="text-blue-600 dark:text-blue-400 hover:underline">
          ← 返回首页
        </Link>
        <button
          onClick={handleSave}
          disabled={saving}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? '保存中...' : '保存论文'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 左侧论文编辑器 */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="论文标题"
            className="w-full text-2xl font-bold mb-4 p-2 border-b border-gray-200 dark:border-gray-700 bg-transparent"
          />

          {/* 编辑器工具栏 */}
          <div className="flex gap-2 mb-4 p-2 bg-gray-100 dark:bg-gray-700 rounded-md">
            <button
              onClick={() => setContent(prev => prev + ' $公式$ ')}
              className="px-3 py-1 text-sm bg-white dark:bg-gray-600 rounded hover:bg-gray-200 dark:hover:bg-gray-500"
            >
              插入公式
            </button>
            <button
              onClick={() => setContent(prev => prev + ' \\begin{align}  \\end{align} ')}
              className="px-3 py-1 text-sm bg-white dark:bg-gray-600 rounded hover:bg-gray-200 dark:hover:bg-gray-500"
            >
              插入多行公式
            </button>
            <button
              onClick={() => document.getElementById('image-upload')?.click()}
              className="px-3 py-1 text-sm bg-white dark:bg-gray-600 rounded hover:bg-gray-200 dark:hover:bg-gray-500"
            >
              插入图片
            </button>
            <input
              type="file"
              id="image-upload"
              accept="image/*"
              className="hidden"
              onChange={handleImageUpload}
            />
          </div>

          <div className="h-[550px] md:h-[450px] sm:h-[350px]">
            <Editor
              height="100%"
              defaultLanguage="markdown"
              value={content}
              onChange={(value) => handleLocalEdit(value)}
              onMount={(editor) => {
                editorRef.current = editor;
                // 监听光标移动事件
                editor.onDidChangeCursorPosition(() => {
                  const position = editor.getPosition();
                  if (position) {
                    const offset = editor.getModel()?.getOffsetAt(position) || 0;
                    handleCursorMove(offset);
                  }
                });
              }}
              options={{
                minimap: { enabled: true },
                scrollBeyondLastLine: false,
                wordWrap: 'on',
              }}
            />
          </div>
        </div>

        {/* 右侧 AI 侧边栏 */}
        <div className="lg:col-span-1 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4">AI 助手</h3>
          
          {/* 实时协作信息 */}
          <div className="mb-4 p-3 bg-gray-100 dark:bg-gray-700 rounded-md">
            <h4 className="font-medium mb-2">实时协作</h4>
            <div className="text-sm">
              <p className="mb-1">当前在线用户: {activeUsers.length}</p>
              {activeUsers.map((userId) => (
                <div key={userId} className="flex items-center mb-1">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                  <span>用户 {userId}</span>
                </div>
              ))}
            </div>
          </div>
          
          {/* 版本管理 */}
          <div className="mb-4">
            <button
              onClick={() => setShowVersions(!showVersions)}
              className="w-full flex justify-between items-center p-2 bg-gray-100 dark:bg-gray-700 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              <span className="font-medium">版本管理</span>
              <span>{showVersions ? '▼' : '▶'}</span>
            </button>
            
            {showVersions && (
              <div className="mt-2 p-3 bg-gray-50 dark:bg-gray-800 rounded-md max-h-60 overflow-y-auto">
                {loadingVersions ? (
                  <p className="text-sm text-gray-500">加载版本历史中...</p>
                ) : versions.length > 0 ? (
                  versions.map((version) => (
                    <div key={version.id} className="mb-3 pb-3 border-b border-gray-200 dark:border-gray-700 last:border-0">
                      <div className="flex justify-between items-start mb-1">
                        <span className="font-medium">版本 {version.version_number}</span>
                        <span className="text-xs text-gray-500">{new Date(version.created_at).toLocaleString()}</span>
                      </div>
                      <p className="text-sm mb-2">创建者: {version.created_by}</p>
                      <button
                        onClick={() => rollbackToVersion(version.id)}
                        className="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700"
                      >
                        回滚到此版本
                      </button>
                    </div>
                  ))
                ) : (
                  <p className="text-sm text-gray-500">暂无版本历史</p>
                )}
              </div>
            )}
          </div>
          
          {/* 模型选择 */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">选择模型</label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200"
            >
              {Object.entries(models).map(([key, model]) => (
                <option key={key} value={key}>
                  {model.name} - {model.description}
                </option>
              ))}
            </select>
          </div>
          
          {/* 深度思考开关 */}
          <div className="mb-4 flex items-center">
            <input
              type="checkbox"
              id="deep-thinking"
              checked={deepThinking}
              onChange={(e) => setDeepThinking(e.target.checked)}
              disabled={!models[selectedModel]?.supports_deep_thinking}
              className="mr-2"
            />
            <label htmlFor="deep-thinking" className={`text-sm ${!models[selectedModel]?.supports_deep_thinking ? 'text-gray-400' : ''}`}>
              深度思考
            </label>
          </div>
          
          {/* AI 功能按钮 */}
          <div className="flex flex-wrap gap-2 mb-4">
            <button
              onClick={handleAiOutline}
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              生成大纲
            </button>
            <button
              onClick={handleAiEdit}
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              AI 编辑
            </button>
            <button
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              润色内容
            </button>
            <button
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              生成引用
            </button>
            <button
              onClick={handleSearchLiterature}
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              查找文献
            </button>
            <button
              onClick={handleSearchGithub}
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              查找代码仓库
            </button>
            <button
              onClick={handleGetPaperOutline}
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              获取章节目录
            </button>
            <button
              onClick={handleGenerateImage}
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              生成图片
            </button>
            <button
              onClick={handleAnalyzeStructure}
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              论文结构分析
            </button>
            <button
              onClick={handleSimulateReview}
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              审稿意见模拟
            </button>
            <button
              onClick={handleGenerateVisualization}
              className="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              数据可视化
            </button>
          </div>

          {/* AI 对话区域 */}
          <div className="h-[400px] md:h-[350px] sm:h-[300px] overflow-y-auto mb-4 border border-gray-200 dark:border-gray-700 rounded-md p-3">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`mb-4 ${message.role === 'user' ? 'flex justify-end' : 'flex justify-start'}`}
              >
                <div
                  className={`max-w-[80%] p-3 rounded-lg ${message.role === 'user' ? 'bg-blue-100 dark:bg-blue-900' : 'bg-gray-100 dark:bg-gray-700'}`}
                >
                  <p>{message.content}</p>
                </div>
              </div>
            ))}
            {aiLoading && (
              <div className="flex justify-start mb-4">
                <div className="max-w-[80%] p-3 rounded-lg bg-gray-100 dark:bg-gray-700">
                  <p>AI 正在思考...</p>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* AI 输入区域 */}
          <div className="flex">
            <input
              type="text"
              value={aiInput}
              onChange={(e) => setAiInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAiSend()}
              placeholder="输入你的问题..."
              className="flex-1 p-2 border border-gray-300 dark:border-gray-600 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleAiSend}
              disabled={aiLoading}
              className="bg-blue-600 text-white px-4 py-2 rounded-r-md hover:bg-blue-700 disabled:opacity-50"
            >
              发送
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PaperEditor;
