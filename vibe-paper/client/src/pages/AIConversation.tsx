import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';

const AIConversation = () => {
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; content: string }[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user' as const, content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // 这里应该调用后端 API 与 AI 对话
      console.log('发送消息:', input);
      // 模拟 AI 回复
      setTimeout(() => {
        const aiMessage = { role: 'assistant' as const, content: `我是 AI 助手，我收到了你的消息：${input}\n\n这里是一些论文写作的建议...` };
        setMessages(prev => [...prev, aiMessage]);
        setLoading(false);
      }, 1000);
    } catch (error) {
      setLoading(false);
      alert('发送失败，请重试');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <Link to="/" className="text-blue-600 dark:text-blue-400 hover:underline">
          ← 返回首页
        </Link>
        <h2 className="text-xl font-semibold">AI 助手</h2>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 h-[600px] flex flex-col">
        <div className="flex-1 overflow-y-auto mb-4">
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
          {loading && (
            <div className="flex justify-start mb-4">
              <div className="max-w-[80%] p-3 rounded-lg bg-gray-100 dark:bg-gray-700">
                <p>AI 正在思考...</p>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="输入你的问题..."
            className="flex-1 p-3 border border-gray-300 dark:border-gray-600 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-3 rounded-r-md hover:bg-blue-700 disabled:opacity-50"
          >
            发送
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIConversation;
